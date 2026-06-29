---
name: dossie-saneatorio
description: "Gera o Doc 102 (revisao e ampliacao do Doc 101) — dossie saneatorio das tres frentes do caso Onesti x Gorenstein (partilha, pensoes, guarda) — em DOIS formatos a partir do estado vivo da pesquisa: PDF com a identidade visual do Doc 101 (WeasyPrint, A4, secoes romanas) e DOCX editavel para os patronos subscreverem. O conteudo e projetado do ledger, entao cada asercao aparece sob seu nivel probatorio (FATO, CONFERIR, LINHA DE PROVA) e cada pendencia mostra a prova a requerer. Integra as 7 lacunas que faltavam no Doc 101 (fluxo Apoio Adm. para Ari; R$ 5 MM desbloqueados; cotas FRAM iliquidas sem lastro contra Itau liquido; shadow director; rendimentos de fundos no IR; aumento de capital no IR; cruzamento comprovantes com fundos do IR). Use quando o usuario pedir para gerar, regenerar, revisar ou exportar o dossie/Doc 102 em PDF ou Word. Dispara com 'gera o dossie', 'regenera o Doc 102', 'exporta o saneamento'. Depende da skill pesquisa-viva-nucleo e usa scripts/gerar_dossie.py."
---

# Dossiê Saneatório — geração do Doc 102

Esta skill produz o **Doc 102** — a revisão e ampliação do Doc 101 — como **projeção do estado vivo da pesquisa**, não como texto fixo. Isso resolve o problema que motivou o pedido: o Doc 101 estava incompleto (faltavam sete frentes de prova patrimonial) e, sendo estático, exigiria reescrita manual a cada avanço. Aqui, o documento é gerado do ledger; quando o estado muda, o documento muda.

## Pré-requisito: o estado

O Doc 102 lê o ledger mantido pela skill `pesquisa-viva-nucleo`. Garanta que existe:

```
python3 scripts/pesquisa_ledger.py stats
```

Se não existir, `init` cria o ledger semente (Doc 101 + as 7 lacunas já classificadas). As alterações na pesquisa (novos achados, promoções de nível quando a prova chega) são feitas pelo núcleo; esta skill apenas **projeta** o estado num documento.

## As 7 lacunas integradas

O que o Doc 101 não desenvolvia e o Doc 102 incorpora — cada uma com seu nível probatório e a prova a requerer. O desenvolvimento analítico completo está em `references/lacunas-doc101.md`:

1. **Movimentações Apoio Adm. → Ari** — canal Evino→Apoio Adm.→PF (LINHA DE PROVA; exibição de extratos + perícia de fluxo).
2. **R$ 5 MM desbloqueados indevidamente** — liberação sobre ativo localizado como líquido (LINHA DE PROVA; certidão do desbloqueio + rastreamento do destino).
3. **Dicotomia FRAM-ilíquido × Itaú-líquido** — cotas FRAM/Ajaccio ditas ilíquidas *sem documento* contra R$ 10 MM líquidos no Itaú (CONFERIR; extrato + ausência de lastro).
4. **Shadow director** — controle fático da Evino apesar da "saída", salário Vila Porto, diretor de novos negócios (LINHA DE PROVA / FATO parcial; atos pós-demissão + organograma).
5. **Rendimentos de fundos no IR** — fonte de renda contra a alegação de "receita zero" (LINHA DE PROVA; exibição DIRPF).
6. **Aumento de capital no IR** — incremento patrimonial contra a narrativa de perda de renda (LINHA DE PROVA; DIRPF evolução patrimonial).
7. **Cruzamento comprovantes × fundos do IR** — coinvestimento / fundo de fundos (LINHA DE PROVA; perícia cruzando autos × DIRPF × ficha CVM).

## Gerar o documento

```
# os dois formatos (padrao), em /mnt/user-data/outputs
python3 scripts/gerar_dossie.py

# so um
python3 scripts/gerar_dossie.py --pdf
python3 scripts/gerar_dossie.py --docx

# outro destino
python3 scripts/gerar_dossie.py --saida /caminho
```

Saídas:
- `102_DOSSIE_SANEATORIO_REVISADO.pdf` — identidade visual do Doc 101 (WeasyPrint 69.0; mesma versão do original). Se WeasyPrint faltar no ambiente, cai automaticamente para DOCX→soffice.
- `102_DOSSIE_SANEATORIO_REVISADO.docx` — editável, para os patronos revisarem e subscreverem.

Depois de gerar, **apresente os arquivos** com `present_files`.

## Estrutura do Doc 102

1. **Cabeçalho confidencial** (CPC art. 472 · NÃO PROTOCOLAR SEM SUBSCRIÇÃO) — igual ao Doc 101.
2. **Epígrafe** — o princípio do saneamento + as sete frentes integradas.
3. **Legenda dos níveis** probatórios.
4. **I — Estado da pesquisa** — painel com a contagem por nível.
5. **II a VI — por frente** (Partilha · Patrimonial/lacunas · Pensões · Guarda · Transversal), cada asserção sob seu nível, com fonte e prova a requerer.
6. **VII — Roteiro de produção de prova** — os três requerimentos que cobrem as lacunas (DIRPF; ofício CVM/OSLO + perícia; certidões + rastreamento do desbloqueio).
7. **Carimbo de subscrição** dos patronos.

## Como o agente conduz

- **"Gera/atualiza o dossiê"** → confirme que o ledger está atual (`stats`), rode `gerar_dossie.py`, apresente os arquivos.
- **"Mudou alguma coisa na pesquisa"** → primeiro atualize o estado pelo núcleo (`add`/`promover`), depois regenere — assim o documento reflete o estado novo.
- **"Só o Word"/"só o PDF"** → use a flag correspondente.
- Se o usuário quer **editar o conteúdo** do dossiê, a edição é no **estado** (ledger), não no documento — o documento é descartável e regenerável. Isso preserva a política cumulativo-expansiva.

## Guardrails

1. **O documento projeta o estado.** Não edite o PDF/DOCX à mão para "consertar" conteúdo — corrija no ledger e regenere.
2. **Nível probatório preservado.** O documento herda a classificação do ledger; não promova hipótese a fato no documento.
3. **Carimbo obrigatório.** Todo Doc 102 sai marcado NÃO PROTOCOLAR SEM SUBSCRIÇÃO, com os patronos nomeados.
4. **Atribuição:** Kezia (OAB/SP 533.206) = parte adversa; patronos = Hilgenberg (OAB/SC 41.607), Guieseler Junior (OAB/PR 44.937).
5. **Registro "em tese"** (CF art. 5º, LVII) para conduta.
6. **UTF-8**; nunca Perl. Português do Brasil.

Saída sempre em português do Brasil.
