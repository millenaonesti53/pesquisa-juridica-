# PORTFÓLIO DE DOSSIÊS — Caso Onesti × Gorenstein
## Índice-mestre, mapa de federação e mapa de processos

> **Método (do plugin `nucleo-forense-gorenstein`):** *federação por referência* — cada análise é indexada uma única vez no dossiê temático que lhe cabe; **não se duplica conteúdo**. Onde havia versões repetidas do mesmo tema (TXT/PDF/HTML/Notion), consolidou-se em **um bloco** com a fonte canônica.
>
> **Sob o [MANIFESTO.md](../../MANIFESTO.md):** partes pelo papel; CPF só do Requerido; **sem CPF da Requerente, sem dados das crianças**; entidades por CNPJ; sem rótulo criminal categórico; **[CONFERIR]** no que depende de fonte oficial.

---

## 1. Estrutura do portfólio (5 dossiês temáticos)

| Dossiê | Tema | Arquivo |
|---|---|---|
| **D1** | Partilha e teia societária (patrimonial) | `01-dossie-partilha-teia-societaria.md` |
| **D2** | Alimentos e capacidade financeira | `02-dossie-alimentos-capacidade.md` |
| **D3** | Guarda, convivência e proteção | `03-dossie-guarda-convivencia.md` |
| **D4** | Inteligência financeira e provas de fraude | `04-dossie-inteligencia-provas.md` |
| **D5** | Frente processual e estratégia | `05-dossie-frente-processual.md` |

Cada dossiê é organizado em **blocos temáticos**; cada bloco tem síntese, fatos-chave (com grau probatório) e **fontes federadas** (nota do repositório + documento(s) de origem).

---

## 2. Mapa de processos (cross-cutting — atualizado)

| Processo | Vara/Foro | Objeto | Estado |
|---|---|---|---|
| **1006738-51**.2023.8.26.0011 | 2ª VF Pinheiros | **Alimentos — sentença 11/04/2024: R$ 24.300/mês + plano de saúde** (título executivo) | Definitivo [CONFERIR] |
| 1006744-58.2023.8.26.0011 | 1ª VF Pinheiros | Divórcio e partilha | Em curso |
| 1007950-39.2025.8.26.0011 | 1ª VF Pinheiros | Cumprimento de sentença (alimentos) | MLE/levantamento |
| 1012537-07.2025.8.26.0011 | 1ª VF Pinheiros | Revisional (redução) de alimentos | Tutela de redução indeferida |
| 0001112-97.2025.8.26.0011 | 1ª VF Pinheiros | Cumprimento c/ SISBAJUD | Bloqueio R$ 42,4 Mi |
| **1166808-32**.2024.8.26.0100 | 9ª VF Central | Guarda e regulamentação de visitas | Astreintes em aberto (vista ao MP) |
| 1050640-10.2025.8.26.0100 | (a esclarecer) | Referido em roteiro HTML | **[CONFERIR]** ação conexa ou erro |

> Detalhe em `pesquisas/mapa-processos-caso.csv`.

---

## 3. Mapa de federação (cada fonte → seu dossiê/bloco; sem duplicar)

| Fonte (acervo recebido) | Dossiê·Bloco | Observação de dedup |
|---|---|---|
| 89 NT Ajaccio cotas/bloqueio · 90 participação real Ari · 93 relatório consolidado Ajaccio/Evino/FRAM/OSLO | D1·B1, B4 | base do parecer-ajaccio + portfolio-financeiro |
| 91 auditoria cronológica · 92 auditoria expandida (hash/carteira) | D1·B1 | resolve [CONFERIR] (Camada 0 FRAM; CNPJs) |
| 94 portfólio por blocos · 97 validação portfólio | D1·B4 | consolidado em consolidacao-97-98-99 |
| 95 capacidade financeira (Laudo Mansano) | D2·B2 | — |
| 96 notificação exibição de NFs / coinvestimento | D2·B4 | grade Mansano |
| 98 laudo gastos das crianças | D2·B3 | transferência ≠ economia |
| 99 diagnóstico e saneamento | D5·B2 | — |
| 71 matriz 16 ações · 72 PIX Porto Seguro · 74-78 cálculos pensão | D2·B5, D4·B4, D5·B1 | 78 traz o título R$ 24.300 |
| 77 relatório IP (criança/Guarujá) | D3·B4 | **dado sensível — manuseio restrito** |
| HTML: Teia Societária, Dossiê Sócio-Financeiro Ajaccio/FRAM, Pareceres Fram/Vinci/Evino, grafos AGEs | D1·B1, B3; D4·B2 | versões Notion — fonte canônica = notas D1/D4 |
| HTML: Matriz de Provas da Fraude, Due Diligence, Background Check, Console Forense | D4·B1, B3 | — |
| HTML: Dossiê do Litígio, Dossiê Sanatório, Caderno de Jurisprudências | D5·B2, B5 | — |
| `nucleo-forense-gorenstein` (plugin/skills) | (método) | não é conteúdo; é a metodologia de federação aplicada |

**Nada foi descartado:** cada documento aponta para um bloco. Versões repetidas (mesmo parecer em TXT+PDF+HTML) entram **uma vez**, na nota canônica.

---

## 4. Integração dos achados NOVOS deste lote

1. **Título executivo dos alimentos** (Doc 78): sentença 11/04/2024 (proc. 1006738-51) — **R$ 24.300/mês + plano de saúde**; alegação de inadimplemento com débito apurado ~**R$ 848 mil** (com CDI). → D2·B1. **Reforça** decisivamente a frente de alimentos e contradiz o pedido de redução a R$ 5.000.
2. **Inconsistência cronológica da AT** (4 análises): faltas alegadas em jan/2026 × AT só deu datas em maio/2026. → D3·B3 (já incorporado ao diagnóstico da guarda v2).
3. **Lógica do MP** sobre proteção × alienação. → D3·B4.
4. **Camada 0 FRAM + CNPJs resolvidos** (Docs 91/92/97). → D1·B1 (já incorporado).

---

## 5. Disciplina anti-excesso (o que foi fundido)

- **3 versões** do diagnóstico da revisional → **1** (nota canônica) + consolidação.
- **Pareceres Fram/Vinci/Ajaccio/Evino** (HTML Notion) → fundidos no **D1·B1/B3** (não reabrir um arquivo por parecer).
- **PACK 73 / dossiês de inteligência** → fatos E1 aproveitados; **quantum maximalista e rótulos descartados** (D4·B5).
- **Cálculos 74-78** → mantém-se **só o Doc 78** como vigente (sucede e revisa 74/76); os demais viram histórico.

---

## 6. Pendências reais (consolidadas)

- Íntegra completa dos autos 1012537-07 e 1166808-32 (peça a peça).
- NFs do relatório Mansano (preencher a grade).
- Esclarecer o processo 1050640-10.2025.
- Certidão oficial dos CNPJs resolvidos por CNPJ-check.
- Confirmar a sentença 1006738-51 (Doc 78) no inteiro teor.
- Documento 77 (IP/criança): manuseio sob segredo; avaliar pertinência e licitude antes de qualquer uso.

---

> **Como navegar:** comece por este índice → vá ao dossiê do tema → cada bloco remete à nota canônica (conteúdo integral) e às fontes de origem. Assim o portfólio é **completo sem ser repetitivo**.
