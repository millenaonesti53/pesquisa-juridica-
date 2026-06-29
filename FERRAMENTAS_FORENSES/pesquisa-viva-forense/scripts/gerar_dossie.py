#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_dossie.py — Gera o Doc 102 (revisao do Doc 101) em DOIS formatos a partir
do estado vivo da pesquisa (estado/pesquisa.json):

  - PDF  : via WeasyPrint, replicando a identidade visual do Doc 101
           (cabecalho confidencial, A4, secoes romanas). Fallback: soffice.
  - DOCX : via docx-js (Node), editavel para os patronos revisarem.

O conteudo NAO e fixo: e projetado do ledger. As 7 lacunas, ja semeadas no
ledger e classificadas por nivel probatorio (FATO / CONFERIR / LINHA_DE_PROVA),
entram automaticamente. O desenvolvimento analitico de cada lacuna vem de
references/lacunas-doc101.md.

Uso:
    python3 gerar_dossie.py            # gera PDF + DOCX em /mnt/user-data/outputs
    python3 gerar_dossie.py --pdf      # so PDF
    python3 gerar_dossie.py --docx     # so DOCX
    python3 gerar_dossie.py --saida /caminho

UTF-8 explicito. Nunca Perl. Marcado NAO PROTOCOLAR SEM SUBSCRICAO.
"""
import sys
import os
import json
import argparse
import subprocess
import tempfile
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(RAIZ, "estado", "pesquisa.json")
SAIDA_PADRAO = "/mnt/user-data/outputs"

CAB = ("CONFIDENCIAL · USO RESTRITO DA EQUIPE · CPC art. 472 · "
       "DOSSIÊ FORENSE DE SANEAMENTO · NÃO PROTOCOLAR SEM SUBSCRIÇÃO")
RODAPE = "CONFIDENCIAL · uso restrito da equipe · Doc 102"
SUBSCRICAO = ("Documento de apoio sujeito à subscrição dos patronos: "
              "Dra. Michele P. Hilgenberg (OAB/SC 41.607) e Dr. Luiz Carlos "
              "Guieseler Junior (OAB/PR 44.937), procuração de 03/06/2026 "
              "(fls. 1065) e CPC art. 112. Preserva-se a presunção de "
              "inocência/boa-fé; tipificações em tese (CF art. 5º, LVII).")

NIVEL_ROTULO = {
    "FATO": "FATO (incontroverso / comprovado nos autos)",
    "CONFERIR": "[CONFERIR] (asseverado · pende fechamento documental)",
    "LINHA_DE_PROVA": "LINHA DE PROVA (hipótese · a confirmar por prova a requerer)",
}
FRENTE_ROTULO = {
    "partilha": "II — Frente 1: Partilha",
    "patrimonial": "III — Eixo Patrimonial / Rastreamento (lacunas do Doc 101)",
    "pensoes": "IV — Frente 2: Pensões / Alimentos",
    "guarda": "V — Frente 3: Guarda / Parental",
    "transversal": "VI — Eixo Transversal: Má-fé e Contaminação",
}
ORDEM_FRENTES = ["partilha", "patrimonial", "pensoes", "guarda", "transversal"]
NIVEIS = ["FATO", "CONFERIR", "LINHA_DE_PROVA"]


def carregar():
    if not os.path.exists(LEDGER):
        print("ERRO: ledger nao existe. Rode antes:")
        print("  python3 scripts/pesquisa_ledger.py init")
        sys.exit(1)
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def agrupar(d):
    """Retorna {frente: {nivel: [asercoes]}}."""
    g = {}
    for a in d["asercoes"]:
        g.setdefault(a["frente"], {}).setdefault(a["nivel"], []).append(a)
    return g


def fila_prova(d):
    return sorted([a for a in d["asercoes"] if a["nivel"] != "FATO"],
                  key=lambda x: (x["nivel"], x["frente"]))


# ──────────────────────────────────────────────────────────────────────────
# PDF via WeasyPrint (identidade visual do Doc 101)
# ──────────────────────────────────────────────────────────────────────────
CSS = """
@page {
  size: A4;
  margin: 2.2cm 1.8cm 2cm 1.8cm;
  @top-center {
    content: "%(cab)s";
    font-size: 6.2pt; letter-spacing: .8px; color: #6b3b16;
    font-family: Georgia, serif;
  }
  @bottom-center {
    content: "%(rodape)s · pág. " counter(page);
    font-size: 6.5pt; color: #888; font-family: Georgia, serif;
  }
}
body { font-family: Georgia, 'Times New Roman', serif; font-size: 9pt;
       color: #1a1a1a; line-height: 1.4; }
h1 { font-size: 16pt; color: #1a1a1a; margin: 0 0 2pt 0; line-height: 1.15; }
.sub { font-size: 8.5pt; color: #444; margin: 0 0 10pt 0; }
.epigrafe { font-style: italic; font-size: 8.5pt; color: #333;
            border-left: 2px solid #9e4e2e; padding: 6pt 10pt; margin: 10pt 0;
            background: #faf6f2; }
h2 { font-size: 11pt; color: #0a2a43; border-bottom: 1px solid #1c4e72;
     padding-bottom: 2pt; margin: 14pt 0 6pt 0; }
h3 { font-size: 9.5pt; color: #1c4e72; margin: 10pt 0 3pt 0; }
.nivel-FATO { color: #1d6f42; }
.nivel-CONFERIR { color: #9e4e2e; }
.nivel-LINHA_DE_PROVA { color: #1c4e72; }
.aid { font-weight: bold; font-size: 8pt; color: #4f5b66; }
ul { margin: 3pt 0 6pt 0; padding-left: 16pt; }
li { margin-bottom: 4pt; }
.fonte { font-size: 7.8pt; color: #666; }
.prova { font-size: 7.8pt; color: #8a3b1e; }
table { width: 100%%; border-collapse: collapse; margin: 6pt 0; font-size: 8pt; }
th, td { border: 1px solid #ccc; padding: 3pt 5pt; text-align: left;
         vertical-align: top; }
th { background: #0a2a43; color: #fff; font-size: 7.8pt; }
.box { background: #f4f7fa; border: 1px solid #1c4e72; border-radius: 3px;
       padding: 8pt 10pt; margin: 8pt 0; font-size: 8.3pt; }
.carimbo { font-size: 7.5pt; color: #6b3b16; font-style: italic;
           border-top: 1px solid #ccc; padding-top: 6pt; margin-top: 12pt; }
.legenda { font-size: 7.8pt; color: #555; background: #f7f7f7;
           border-radius: 3px; padding: 6pt 8pt; margin: 8pt 0; }
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def html_doc(d):
    g = agrupar(d)
    porn = {n: sum(1 for a in d["asercoes"] if a["nivel"] == n) for n in NIVEIS}
    H = []
    H.append("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>")
    H.append("<h1>Dossiê Saneatório dos Processos — Partilha · Guarda · Pensões</h1>")
    H.append("<p class='sub'>Visão forense unificada · caso Onesti × Gorenstein · "
             "proc. 1006744-58.2023 (divórcio/partilha) + 1012537-07.2025 "
             "(revisional) + frentes de guarda/protetivas<br>"
             "<b>Documento 102</b> · revisão e ampliação do Doc 101 · "
             f"gerado em {datetime.now().strftime('%d/%m/%Y')} · "
             "parecer de PhD perito forense</p>")
    H.append("<div class='epigrafe'>Sanear é separar o que já está provado do que "
             "ainda precisa ser provado. Esta revisão integra ao Doc 101 as sete "
             "frentes de prova patrimonial que faltavam: o fluxo Apoio Adm.→PF, "
             "os R$ 5 milhões desbloqueados sobre ativo líquido, a dicotomia "
             "FRAM-sem-lastro × Itaú-líquido, a função de shadow director, e o "
             "cruzamento IR × fundos (rendimentos, aumento de capital, "
             "coinvestimento).</div>")
    # legenda dos niveis
    H.append("<div class='legenda'><b>Níveis probatórios:</b> "
             "<span class='nivel-FATO'>FATO</span> = comprovante nos autos · "
             "<span class='nivel-CONFERIR'>[CONFERIR]</span> = asseverado, pende "
             "certidão/documento · "
             "<span class='nivel-LINHA_DE_PROVA'>LINHA DE PROVA</span> = hipótese "
             "a confirmar por prova a requerer.</div>")
    # painel de estado
    H.append("<h2>I — Estado da pesquisa (projeção do estado vivo)</h2>")
    H.append("<table><tr><th>Nível</th><th>Asserções</th><th>Significado operacional</th></tr>")
    H.append(f"<tr><td class='nivel-FATO'>FATO</td><td>{porn['FATO']}</td>"
             "<td>Sustentam pedido; citáveis com fls.</td></tr>")
    H.append(f"<tr><td class='nivel-CONFERIR'>[CONFERIR]</td><td>{porn['CONFERIR']}</td>"
             "<td>Não usar como incontroverso até promover.</td></tr>")
    H.append(f"<tr><td class='nivel-LINHA_DE_PROVA'>LINHA DE PROVA</td>"
             f"<td>{porn['LINHA_DE_PROVA']}</td>"
             "<td>Viram pedidos de produção de prova no saneamento.</td></tr>")
    H.append("</table>")
    # por frente
    for fr in ORDEM_FRENTES:
        if fr not in g:
            continue
        H.append(f"<h2>{esc(FRENTE_ROTULO[fr])}</h2>")
        for nivel in NIVEIS:
            grupo = g[fr].get(nivel, [])
            if not grupo:
                continue
            H.append(f"<h3 class='nivel-{nivel}'>{esc(NIVEL_ROTULO[nivel])}</h3><ul>")
            for a in grupo:
                H.append(f"<li><span class='aid'>[{a['id']}]</span> {esc(a['asercao'])}")
                if a["fonte"]:
                    H.append(f"<br><span class='fonte'>Fonte: {esc(a['fonte'])}</span>")
                if nivel != "FATO" and a["prova_necessaria"]:
                    H.append(f"<br><span class='prova'>▸ Prova a requerer: "
                             f"{esc(a['prova_necessaria'])}</span>")
                H.append("</li>")
            H.append("</ul>")
    # fila de prova consolidada
    fila = fila_prova(d)
    H.append("<h2>VII — Roteiro de produção de prova (saneamento CPC 357)</h2>")
    H.append("<div class='box'>As pendências convergem em três requerimentos que "
             "servem a múltiplas frentes:<br>"
             "<b>1. Exibição da DIRPF completa de Ari</b> — rendimentos de fundos, "
             "aumento de capital, fundos para cruzamento (lacunas 5, 6, 7).<br>"
             "<b>2. Ofício CVM/OSLO + perícia contábil única (CPC 464)</b> — ficha "
             "de cotistas, fluxo Apoio Adm.→PF, natureza das cotas FRAM, "
             "coinvestimento (lacunas 1, 3, 4, 7).<br>"
             "<b>3. Certidões e rastreamento do desbloqueio</b> — destino dos "
             "R$ 5 MM e reconstituição da constrição (lacuna 2).</div>")
    H.append(f"<p style='font-size:8pt'><b>Fila completa ({len(fila)} pendências):</b></p><ul>")
    for a in fila:
        H.append(f"<li><span class='aid'>[{a['id']}]</span> ({a['frente']}) "
                 f"{esc(a['prova_necessaria'] or '[definir]')}</li>")
    H.append("</ul>")
    # carimbo
    H.append(f"<p class='carimbo'>{esc(SUBSCRICAO)}</p>")
    H.append("</body></html>")
    return "\n".join(H)


def gerar_pdf(d, saida):
    destino = os.path.join(saida, "102_DOSSIE_SANEATORIO_REVISADO.pdf")
    html = html_doc(d)
    css = CSS % {"cab": CAB, "rodape": RODAPE}
    try:
        from weasyprint import HTML, CSS as WCSS
        HTML(string=html).write_pdf(destino, stylesheets=[WCSS(string=css)])
        print(f"[PDF] WeasyPrint -> {destino}")
        return destino
    except Exception as e:
        print(f"[PDF] WeasyPrint indisponivel ({e}); tentando via DOCX->soffice...")
        docx = gerar_docx(d, saida)
        try:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                            "--outdir", saida, docx], check=True,
                           capture_output=True, timeout=120)
            print(f"[PDF] soffice -> {destino}")
        except Exception as e2:
            print(f"[PDF] FALHOU: {e2}")
            return None
        return destino


# ──────────────────────────────────────────────────────────────────────────
# DOCX via docx-js (Node) — editavel para os patronos
# ──────────────────────────────────────────────────────────────────────────
def gerar_docx(d, saida):
    destino = os.path.join(saida, "102_DOSSIE_SANEATORIO_REVISADO.docx")
    payload = {
        "gerado": datetime.now().strftime("%d/%m/%Y"),
        "cab": CAB, "rodape": RODAPE, "subscricao": SUBSCRICAO,
        "frentes": [], "fila": [],
    }
    g = agrupar(d)
    for fr in ORDEM_FRENTES:
        if fr not in g:
            continue
        bloco = {"titulo": FRENTE_ROTULO[fr], "niveis": []}
        for nivel in NIVEIS:
            grupo = g[fr].get(nivel, [])
            if not grupo:
                continue
            bloco["niveis"].append({
                "rotulo": NIVEL_ROTULO[nivel], "nivel": nivel,
                "itens": [{"id": a["id"], "asercao": a["asercao"],
                           "fonte": a["fonte"],
                           "prova": a["prova_necessaria"] if nivel != "FATO" else ""}
                          for a in grupo]
            })
        payload["frentes"].append(bloco)
    payload["fila"] = [{"id": a["id"], "frente": a["frente"],
                        "prova": a["prova_necessaria"] or "[definir]"}
                       for a in fila_prova(d)]

    js = r'''
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, LevelFormat, PageNumber } = require('docx');
const P = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const COR = { FATO: "1D6F42", CONFERIR: "9E4E2E", LINHA_DE_PROVA: "1C4E72" };
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const children = [];
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1,
  children: [new TextRun("Dossie Saneatorio — Partilha · Guarda · Pensoes (Doc 102)")] }));
children.push(new Paragraph({ children: [new TextRun({
  text: "Caso Onesti × Gorenstein · proc. 1006744-58.2023 + 1012537-07.2025 · revisao e ampliacao do Doc 101 · gerado em " + P.gerado,
  italics: true, size: 17, color: "444444" })] }));
children.push(new Paragraph({ spacing: { before: 120, after: 120 },
  border: { left: { style: BorderStyle.SINGLE, size: 12, color: "9E4E2E", space: 8 } },
  children: [new TextRun({ italics: true, size: 17, color: "333333",
  text: "Sanear e separar o que ja esta provado do que ainda precisa ser provado. Esta revisao integra ao Doc 101 as sete frentes de prova patrimonial que faltavam." })] }));
// legenda
children.push(new Paragraph({ shading: { fill: "F2F2F2", type: ShadingType.CLEAR },
  spacing: { after: 120 }, children: [
  new TextRun({ text: "Niveis probatorios: ", bold: true, size: 16 }),
  new TextRun({ text: "FATO", bold: true, color: COR.FATO, size: 16 }),
  new TextRun({ text: " = comprovante nos autos · ", size: 16 }),
  new TextRun({ text: "[CONFERIR]", bold: true, color: COR.CONFERIR, size: 16 }),
  new TextRun({ text: " = pende certidao/documento · ", size: 16 }),
  new TextRun({ text: "LINHA DE PROVA", bold: true, color: COR.LINHA_DE_PROVA, size: 16 }),
  new TextRun({ text: " = a confirmar por prova a requerer.", size: 16 }),
] }));

P.frentes.forEach(fr => {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_2,
    spacing: { before: 220, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1C4E72", space: 2 } },
    children: [new TextRun({ text: fr.titulo, color: "0A2A43" })] }));
  fr.niveis.forEach(nv => {
    children.push(new Paragraph({ spacing: { before: 100, after: 40 },
      children: [new TextRun({ text: nv.rotulo, bold: true, size: 19, color: COR[nv.nivel] || "000000" })] }));
    nv.itens.forEach(it => {
      const runs = [
        new TextRun({ text: "[" + it.id + "] ", bold: true, size: 16, color: "4F5B66" }),
        new TextRun({ text: it.asercao, size: 18 }),
      ];
      children.push(new Paragraph({ numbering: { reference: "bul", level: 0 },
        spacing: { after: 20 }, children: runs }));
      if (it.fonte)
        children.push(new Paragraph({ indent: { left: 720 },
          children: [new TextRun({ text: "Fonte: " + it.fonte, size: 15, color: "666666" })] }));
      if (it.prova)
        children.push(new Paragraph({ indent: { left: 720 }, spacing: { after: 40 },
          children: [new TextRun({ text: "▸ Prova a requerer: " + it.prova, size: 15, color: "8A3B1E" })] }));
    });
  });
});

// roteiro
children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 220, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1C4E72", space: 2 } },
  children: [new TextRun({ text: "Roteiro de producao de prova (CPC 357)", color: "0A2A43" })] }));
[["1. Exibicao da DIRPF completa de Ari","rendimentos de fundos, aumento de capital, fundos para cruzamento (lacunas 5, 6, 7)"],
 ["2. Oficio CVM/OSLO + pericia contabil unica (CPC 464)","ficha de cotistas, fluxo Apoio Adm.->PF, natureza das cotas FRAM, coinvestimento (lacunas 1, 3, 4, 7)"],
 ["3. Certidoes e rastreamento do desbloqueio","destino dos R$ 5 MM e reconstituicao da constricao (lacuna 2)"]
].forEach(([t,s]) => {
  children.push(new Paragraph({ numbering: { reference: "num", level: 0 }, spacing: { after: 40 },
    children: [new TextRun({ text: t + " — ", bold: true, size: 18 }),
               new TextRun({ text: s, size: 18 })] }));
});

// carimbo
children.push(new Paragraph({ spacing: { before: 240 },
  border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 6 } },
  children: [new TextRun({ text: P.subscricao, italics: true, size: 15, color: "6B3B16" })] }));

const doc = new Document({
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] },
  ] },
  styles: { default: { document: { run: { font: "Georgia", size: 18 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Georgia", color: "0A2A43" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Georgia", color: "0A2A43" },
        paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 } },
    ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 },
      margin: { top: 1300, right: 1080, bottom: 1150, left: 1080 } } },
    headers: { default: new Header({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: P.cab, size: 12, color: "6B3B16" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: P.rodape + " · pag. ", size: 13, color: "888888" }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 13, color: "888888" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[3], b);
  console.log("[DOCX] gerado -> " + process.argv[3]); });
'''
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as jf:
        json.dump(payload, jf, ensure_ascii=False)
        jpath = jf.name
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as sf:
        sf.write(js)
        spath = sf.name
    try:
        env = dict(os.environ, NODE_PATH=subprocess.run(
            ["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
        r = subprocess.run(["node", spath, jpath, destino], capture_output=True,
                           text=True, env=env, timeout=120)
        if r.stdout.strip():
            print(r.stdout.strip())
        if r.returncode != 0:
            print("[DOCX] ERRO:", r.stderr[:800])
            return None
    finally:
        os.unlink(jpath)
        os.unlink(spath)
    return destino


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--docx", action="store_true")
    ap.add_argument("--saida", default=SAIDA_PADRAO)
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    d = carregar()
    so_um = a.pdf ^ a.docx
    if a.docx and so_um:
        gerar_docx(d, a.saida)
    elif a.pdf and so_um:
        gerar_pdf(d, a.saida)
    else:
        gerar_docx(d, a.saida)
        gerar_pdf(d, a.saida)


if __name__ == "__main__":
    main()
