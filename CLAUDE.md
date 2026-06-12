# pesquisa-juridica-

Repositório para pesquisas jurídicas ampliadas e aprofundadas.

## Propósito
Apoiar a produção de notas técnicas, pareceres e relatórios analítico-sanatórios em matéria jurídica, com foco em análise documental (PDFs, decisões, regulamentos) e organização de evidências.

## Convenções para o Claude
- Idioma padrão das respostas e commits: **português (Brasil)**.
- Citações jurídicas devem manter formatação original (lei/artigo/inciso, jurisprudência com tribunal e número).
- Nunca inventar números de processo, datas ou trechos de acórdão — se não houver fonte no repo, declarar explicitamente.
- Documentos sensíveis (CPF, CNPJ, dados patrimoniais) devem ser tratados como confidenciais; não publicar em PRs nem em commits.
- Quando solicitada uma nota técnica ou parecer, estruturar em: (1) síntese, (2) fatos, (3) fundamentação, (4) conclusão.

## Estrutura sugerida
- `documentos/` — PDFs e fontes primárias (não versionar conteúdo sensível)
- `notas/` — notas técnicas e pareceres em markdown
- `pesquisas/` — levantamentos jurisprudenciais e doutrinários

## Setup
A extensão Claude Code para VS Code é recomendada (ver `.vscode/extensions.json`).
