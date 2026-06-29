#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pesquisa_ledger.py — Motor de estado da pesquisa forense viva.

Mantem a pesquisa do caso Onesti x Gorenstein como ESTADO VIVO, versionavel e
validavel, em vez de um dossie estatico que envelhece. Cada asercao da pesquisa
e uma entrada com:
  - nivel probatorio: FATO | CONFERIR | LINHA_DE_PROVA
  - frente: partilha | pensoes | guarda | transversal | patrimonial
  - fonte (fls., Doc, peticao) e a prova que a sustenta (ou que falta)
  - status de validacao e historico de mudancas (cumulativo-expansivo)

Regra probatoria (fixada pela usuaria):
  FATO          = ha comprovante nos autos (confissao em peticao, doc juntado,
                  decisao). Citavel.
  CONFERIR      = asseverado nas minutas, sem certidao/documento que feche.
  LINHA_DE_PROVA= hipotese de investigacao; depende de prova a requerer
                  (oficio, exibicao, pericia).

Nunca deleta asercao validada (politica cumulativo-expansiva): muda de nivel,
registra o motivo e a data. O historico fica.

Uso:
    python3 pesquisa_ledger.py init                    # cria o ledger semente
    python3 pesquisa_ledger.py list [--frente X] [--nivel Y]
    python3 pesquisa_ledger.py add --frente partilha --nivel LINHA_DE_PROVA \\
        --asercao "..." --fonte "..." --prova-necessaria "..."
    python3 pesquisa_ledger.py promover --id AS0012 --para FATO \\
        --motivo "Certidao TJMS juntada fls. X"
    python3 pesquisa_ledger.py stats                   # contagem por nivel/frente
    python3 pesquisa_ledger.py lacunas                 # so LINHA_DE_PROVA + CONFERIR
    python3 pesquisa_ledger.py export-md > dossie.md   # regenera o dossie

Sem dependencia externa. UTF-8 explicito. Nunca Perl.
"""
import sys
import os
import json
import argparse
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESTADO_DIR = os.path.join(RAIZ, "estado")
LEDGER = os.path.join(ESTADO_DIR, "pesquisa.json")

NIVEIS = ("FATO", "CONFERIR", "LINHA_DE_PROVA")
FRENTES = ("partilha", "pensoes", "guarda", "transversal", "patrimonial")


def _hoje():
    return date.today().isoformat()


def _load():
    if not os.path.exists(LEDGER):
        return None
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def _save(d):
    os.makedirs(ESTADO_DIR, exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def _novo(d, frente, nivel, asercao, fonte="", prova_nec="", obs=""):
    d["seq"] += 1
    aid = f"AS{d['seq']:04d}"
    entrada = {
        "id": aid,
        "frente": frente,
        "nivel": nivel,
        "asercao": asercao,
        "fonte": fonte,
        "prova_necessaria": prova_nec,
        "obs": obs,
        "criado": _hoje(),
        "historico": [{"data": _hoje(), "evento": "criada", "nivel": nivel}],
    }
    d["asercoes"].append(entrada)
    return aid


# ──────────────────────────────────────────────────────────────────────────
# SEMENTE — conteudo do Doc 101 + as 7 lacunas apontadas pela usuaria
# Classificacao mista: o que tem comprovante nos autos = FATO; o asseverado
# sem fechamento = CONFERIR; a hipotese de investigacao = LINHA_DE_PROVA.
# ──────────────────────────────────────────────────────────────────────────
def _semente(d):
    F, C, L = "FATO", "CONFERIR", "LINHA_DE_PROVA"

    seed = [
        # ---- PARTILHA: confissoes do reu (FATO) ----
        (("partilha", F,
          "Renda do reu de R$ 50.000/mes (Vila Porto International Business S.A.)",
          "reconvencao 1012537-07.2025", "",
          "Confissao em peticao do proprio reu.")),
        (("partilha", F,
          "Patrimonio do reu > R$ 32.000.000,00",
          "contestacao/reconvencao", "",
          "Confissao em peticao.")),
        (("partilha", F,
          "Oferta de aquisicao das cotas por > R$ 4.000.000,00 (Operacao Ricardo)",
          "Doc 90", "", "")),
        (("partilha", C,
          "Reu e representante legal da Evino em processo ativo (TJMS 0926609-45.2024) "
          "apesar da alegada saida",
          "Doc 100 / Exato PF", "Certidao de objeto e pe TJMS 0926609-45.2024",
          "Asseverado; pende certidao para fechar como FATO oponivel.")),
        # ---- PARTILHA: controvertidos / onus ----
        (("partilha", L,
          "Valor e titularidade das cotas de Ari (Classes A+F, ~4,42%) no Ajaccio",
          "—", "Oficio CVM/OSLO: ficha de cotistas, valor e datas das cotas",
          "Inversao do onus pretendida (assimetria + retencao + CNJ 492/2023).")),
        (("partilha", C,
          "Iliquidez do FIP afirmada sem prova (sem politica/laudo/ata)",
          "fls. 1421-1423", "Exibicao do Acordo de Cotistas (Cl. 9.7, 10.1.7) e laudo",
          "Afirmacao do reu desacompanhada de lastro documental.")),
        # ---- LACUNA 3: a DICOTOMIA precisa (ilicito x liquido) ----
        (("patrimonial", C,
          "Dicotomia dos ativos no SISBAJUD: a pesquisa retornou CAIXA, nao cotas. "
          "Ativos do CPF tratados como 'cotas iliquidas' sao, na origem, liquidez.",
          "Docs 89/90/93", "Detalhamento SISBAJUD por instituicao e natureza do ativo",
          "Nucleo da contradicao 'iliquido la, liquido aqui'.")),
        (("patrimonial", C,
          "Ativos liquidos localizados: Itau ~R$ 10.000.000,00 (liquido), em contraste "
          "com cotas FRAM/Ajaccio apresentadas como iliquidas SEM documento comprobatorio",
          "[CONFERIR fls.]", "Extrato Itau + ausencia de lastro das cotas FRAM no SISBAJUD",
          "LACUNA 3: contraste FRAM-sem-lastro x Itau-liquido a desenvolver.")),
        (("patrimonial", F,
          "SISBAJUD localizou caixa de R$ 84,8 MM (nao cotas) no ambito da pesquisa",
          "Docs 89/90/93", "",
          "Ja afirmado no Doc 101 como achado da pesquisa SISBAJUD.")),
        # ---- LACUNA 2: os 5M desbloqueados indevidamente ----
        (("patrimonial", L,
          "R$ 5.000.000,00 desbloqueados indevidamente apos a dicotomia dos ativos "
          "(liberacao de numerario localizado como liquido, em desacordo com a constricao)",
          "[CONFERIR fls. da decisao/peticao de desbloqueio]",
          "Certidao da decisao de desbloqueio + extrato do fluxo dos R$ 5 MM apos liberacao",
          "LACUNA 2: ausente no Doc 101. Cruzar com o padrao de desbloqueio coordenado.")),
        # ---- LACUNA 1: fluxo Apoio Adm. -> Ari ----
        (("patrimonial", L,
          "Movimentacoes da Apoio Administrativa para Ari (fluxo Evino -> Apoio Adm. -> PF) "
          "como canal de transferencia de recursos a pessoa fisica",
          "Doc 101 II.5/VII (citado, nao desenvolvido)",
          "Exibicao de extratos da Apoio Adm.; pericia de reconstituicao do fluxo",
          "LACUNA 1: condicionado a juntada de extrato (calibracao 02 herdada).")),
        # ---- LACUNA 4: shadow director ----
        (("patrimonial", L,
          "Funcao de shadow director: Ari mantem controle fatico/gestao da Evino e do grupo "
          "apesar da 'saida' formal, com salario Vila Porto e papel de diretor de novos negocios",
          "Doc 100 (representante 2026); contrato Vila Porto 01/07/2025",
          "Atos societarios assinados pos-demissao; organograma; e-mails/atas de gestao",
          "LACUNA 4: nomear como TESE de shadow director, nao so 'vinculo Vila Porto'.")),
        (("pensoes", F,
          "Contrato Vila Porto Vinhos (mesmo setor; R$ 50k/mes) firmado 01/07/2025, "
          "viola a propria nao-concorrencia e estabelece renda nova",
          "contrato 01/07/2025", "",
          "Ja no Doc 101 III.2.")),
        # ---- LACUNA 5: rendimentos de fundos no IR ----
        (("patrimonial", L,
          "Rendimentos de fundos declarados no IR de Ari (existencia e magnitude) — "
          "fonte de renda/patrimonio nao refletida na alegacao de 'receita zero'",
          "[CONFERIR DIRPF Ari]",
          "Exibicao da DIRPF completa (fichas de rendimentos e bens) + cruzamento",
          "LACUNA 5: ausente no Doc 101.")),
        # ---- LACUNA 6: aumento de capital no IR ----
        (("patrimonial", L,
          "Aumento de capital declarado no IR de Ari — incremento patrimonial que "
          "contradiz a narrativa de perda de renda",
          "[CONFERIR DIRPF Ari]",
          "Exibicao da DIRPF (evolucao patrimonial ano a ano); confronto com os atos societarios",
          "LACUNA 6: ausente no Doc 101.")),
        # ---- LACUNA 7: cruzar comprovantes x fundos do IR (coinvestimento / fundo de fundos) ----
        (("patrimonial", L,
          "Cruzamento dos comprovantes trazidos no processo com os fundos registrados no IR: "
          "suspeita de coinvestimento nos fundos e/ou estrutura de fundos de fundos",
          "comprovantes nos autos [CONFERIR fls.] + DIRPF",
          "Pericia cruzando comprovantes processuais x fundos da DIRPF x ficha de cotistas CVM",
          "LACUNA 7: tese de investigacao nova — coinvestimento / fundo de fundos.")),
        # ---- PENSOES: estado e ma-fe (FATO) ----
        (("pensoes", F,
          "Tutela de reducao de alimentos INDEFERIDA; prisao civil do reu por inadimplemento decretada",
          "fls. 375/376; parecer MP fls. 1544/1546; fls. 1545", "", "")),
        (("pensoes", F,
          "Padrao de cronometragem: 'demissao' da Evino em 02/12/2024, 3 dias antes da peticao "
          "de 05/12/2024 alegando 'receita zero'; non-compete R$ 749.183,38 em 29/01/2025",
          "autos revisional", "",
          "Sustenta litigancia de ma-fe (CPC 80, II) e presuncao art. 400.")),
        (("pensoes", F,
          "MP reconheceu: mensalidade menor (Camino->Modulo) != custo menor das criancas",
          "fls. 1544/1546", "",
          "Nucleo contabil ja acolhido pelo MP.")),
        # ---- GUARDA ----
        (("guarda", F,
          "Guarda e visitas suspensas desde out/2024; medidas protetivas vigentes; IP em curso",
          "decisao out/2024; autos protetivas", "",
          "Afastamento imposto pelo Estado — ilicito imputavel e a conduta dolosa anterior.")),
        (("guarda", C,
          "Uniao formal de Ari com filha de pessoa sob investigacao por suposto ilicito contra Caio "
          "como fato novo material",
          "[CONFERIR documento da uniao]", "Certidao/prova da uniao + do IP correlato",
          "Mencionado no acervo; pende fechamento documental.")),
        # ---- TRANSVERSAL: matriz de contradicoes ----
        (("transversal", F,
          "Cinco alegacoes do reu contraditadas por prova (saida Evino; cotas iliquidas; "
          "receita zero; queda de gastos; ausencia de violencia) — autoriza reconhecimento do padrao",
          "Doc 101 secao V", "",
          "Pede-se reconhecimento do PADRAO, nao nulidade global.")),
    ]
    for args in seed:
        _novo(d, *args)


def cmd_init(_):
    if os.path.exists(LEDGER):
        print(f"Ledger ja existe: {LEDGER}. Use 'list' ou 'stats'.")
        return
    d = {"caso": "Onesti x Gorenstein",
         "processos": ["1006744-58.2023.8.26.0011", "1012537-07.2025.8.26.0011"],
         "sucede": "Doc 101", "seq": 0, "asercoes": []}
    _semente(d)
    _save(d)
    print(f"Ledger semente criado: {LEDGER}")
    print(f"  {len(d['asercoes'])} asercoes carregadas (Doc 101 + 7 lacunas).")
    _print_stats(d)


def _print_stats(d):
    porn = {n: 0 for n in NIVEIS}
    porf = {}
    for a in d["asercoes"]:
        porn[a["nivel"]] = porn.get(a["nivel"], 0) + 1
        porf[a["frente"]] = porf.get(a["frente"], 0) + 1
    print("  Por nivel:", " | ".join(f"{k}={v}" for k, v in porn.items()))
    print("  Por frente:", " | ".join(f"{k}={v}" for k, v in porf.items()))


def cmd_stats(_):
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    print(f"Caso: {d['caso']} | asercoes: {len(d['asercoes'])}")
    _print_stats(d)


def cmd_list(a):
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    items = d["asercoes"]
    if a.frente:
        items = [x for x in items if x["frente"] == a.frente]
    if a.nivel:
        items = [x for x in items if x["nivel"] == a.nivel]
    if not items:
        print("(nenhuma asercao com esse filtro)")
        return
    for x in items:
        print(f"\n[{x['id']}] {x['frente'].upper()} · {x['nivel']}")
        print(f"  {x['asercao']}")
        if x["fonte"]:
            print(f"  fonte: {x['fonte']}")
        if x["nivel"] != "FATO" and x["prova_necessaria"]:
            print(f"  prova necessaria: {x['prova_necessaria']}")


def cmd_lacunas(_):
    """So o que ainda nao e FATO — a fila de producao de prova."""
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    pend = [x for x in d["asercoes"] if x["nivel"] != "FATO"]
    pend.sort(key=lambda x: (x["nivel"], x["frente"]))
    print(f"== Fila de producao de prova ({len(pend)} pendencia(s)) ==")
    for x in pend:
        print(f"\n[{x['id']}] {x['frente'].upper()} · {x['nivel']}")
        print(f"  {x['asercao']}")
        print(f"  -> prova necessaria: {x['prova_necessaria'] or '[definir]'}")


def cmd_add(a):
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    if a.nivel not in NIVEIS:
        print(f"ERRO: nivel deve ser {NIVEIS}")
        sys.exit(2)
    if a.frente not in FRENTES:
        print(f"ERRO: frente deve ser {FRENTES}")
        sys.exit(2)
    aid = _novo(d, a.frente, a.nivel, a.asercao, a.fonte or "",
                a.prova_necessaria or "", a.obs or "")
    _save(d)
    print(f"Asercao {aid} adicionada ({a.frente} · {a.nivel}).")


def cmd_promover(a):
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    if a.para not in NIVEIS:
        print(f"ERRO: --para deve ser {NIVEIS}")
        sys.exit(2)
    for x in d["asercoes"]:
        if x["id"] == a.id:
            antigo = x["nivel"]
            x["nivel"] = a.para
            x["historico"].append({"data": _hoje(), "evento": "mudanca_nivel",
                                    "de": antigo, "para": a.para, "motivo": a.motivo or ""})
            _save(d)
            print(f"{a.id}: {antigo} -> {a.para} ({a.motivo or 'sem motivo'})")
            return
    print(f"ERRO: asercao {a.id} nao encontrada.")
    sys.exit(2)


def cmd_export_md(_):
    d = _load()
    if not d:
        print("Ledger nao existe. Rode 'init'.")
        sys.exit(1)
    from datetime import datetime
    out = []
    out.append("# Dossie Saneatorio — estado vivo da pesquisa")
    out.append(f"\n**Caso:** {d['caso']} · **Processos:** {', '.join(d['processos'])}  ")
    out.append(f"**Gerado:** {datetime.now().strftime('%d/%m/%Y %H:%M')} · sucede {d.get('sucede','-')}  ")
    out.append("**CONFIDENCIAL · USO RESTRITO DA EQUIPE · CPC art. 472 · "
               "NAO PROTOCOLAR SEM SUBSCRICAO**\n")
    # legenda
    out.append("> Niveis: **FATO** = comprovante nos autos · "
               "**[CONFERIR]** = asseverado, pende certidao/documento · "
               "**LINHA DE PROVA** = hipotese a confirmar por prova a requerer.\n")
    rotulo = {"partilha": "Partilha", "pensoes": "Pensoes / Alimentos",
              "guarda": "Guarda / Parental", "patrimonial": "Eixo Patrimonial / Rastreamento",
              "transversal": "Eixo Transversal (ma-fe)"}
    for fr in ("partilha", "patrimonial", "pensoes", "guarda", "transversal"):
        its = [x for x in d["asercoes"] if x["frente"] == fr]
        if not its:
            continue
        out.append(f"\n## {rotulo[fr]}\n")
        for nivel in NIVEIS:
            grupo = [x for x in its if x["nivel"] == nivel]
            if not grupo:
                continue
            tag = {"FATO": "FATO (incontroverso / comprovado)",
                   "CONFERIR": "[CONFERIR] (pende fechamento documental)",
                   "LINHA_DE_PROVA": "LINHA DE PROVA (a requerer)"}[nivel]
            out.append(f"### {tag}\n")
            for x in grupo:
                out.append(f"- **[{x['id']}]** {x['asercao']}")
                if x["fonte"]:
                    out.append(f"  - Fonte: {x['fonte']}")
                if nivel != "FATO" and x["prova_necessaria"]:
                    out.append(f"  - Prova necessaria: {x['prova_necessaria']}")
            out.append("")
    # fila de prova
    pend = [x for x in d["asercoes"] if x["nivel"] != "FATO"]
    out.append(f"\n## Fila de producao de prova ({len(pend)} pendencia(s))\n")
    for x in sorted(pend, key=lambda x: (x["nivel"], x["frente"])):
        out.append(f"- **[{x['id']}]** ({x['frente']}) {x['prova_necessaria'] or '[definir]'}")
    out.append("\n---\n*Documento de apoio sujeito a subscricao dos patronos "
               "(Hilgenberg OAB/SC 41.607; Guieseler Junior OAB/PR 44.937). "
               "Tipificacoes em tese (CF art. 5 LVII).*")
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description="Motor de estado da pesquisa forense viva.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("stats")
    sub.add_parser("lacunas")
    sub.add_parser("export-md")
    pl = sub.add_parser("list")
    pl.add_argument("--frente", choices=FRENTES)
    pl.add_argument("--nivel", choices=NIVEIS)
    pa = sub.add_parser("add")
    pa.add_argument("--frente", required=True, choices=FRENTES)
    pa.add_argument("--nivel", required=True, choices=NIVEIS)
    pa.add_argument("--asercao", required=True)
    pa.add_argument("--fonte", default="")
    pa.add_argument("--prova-necessaria", dest="prova_necessaria", default="")
    pa.add_argument("--obs", default="")
    pp = sub.add_parser("promover")
    pp.add_argument("--id", required=True)
    pp.add_argument("--para", required=True, choices=NIVEIS)
    pp.add_argument("--motivo", default="")
    a = ap.parse_args()
    {
        "init": cmd_init, "stats": cmd_stats, "list": cmd_list,
        "lacunas": cmd_lacunas, "add": cmd_add, "promover": cmd_promover,
        "export-md": cmd_export_md,
    }[a.cmd.replace("-", "_") if a.cmd == "export-md" else a.cmd](a)


if __name__ == "__main__":
    # mapeia 'export-md' para a funcao
    if len(sys.argv) > 1 and sys.argv[1] == "export-md":
        d = _load()
        if not d:
            print("Ledger nao existe. Rode 'init'."); sys.exit(1)
        cmd_export_md(None); sys.exit(0)
    main()
