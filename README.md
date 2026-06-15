# pesquisa-juridica-

Repositório para pesquisas jurídicas ampliadas e aprofundadas, com foco em investigação patrimonial, análise documental e produção de notas técnicas e pareceres.

## Pipeline Cognitivo Corporativo

Sistema integrado de investigação patrimonial automatizada:

| Módulo | Função |
|--------|--------|
| [Briefing](pipeline/01-briefing.md) | Inteligência diária — CVM, SISBAJUD, bancos, FIPs |
| [Health Check](pipeline/02-health-check.md) | Consistência de PLs, divergências IRPF × CVM, ocultação |
| [Dependency Update](pipeline/03-dependency-update.md) | Atualização de bases, detecção de alterações suspeitas |
| [Flaky Tracker](pipeline/04-flaky-tracker.md) | Validação estatística, esvaziamento tático, padrões de fraude |
| [PR Review Digest](pipeline/05-pr-review-digest.md) | Relatórios CLO, pareceres IDPJ, minutas COAF/MPF |

Arquitetura completa: [`pipeline/00-pipeline-cognitivo-corporativo.md`](pipeline/00-pipeline-cognitivo-corporativo.md)

## Estrutura

```
documentos/   — PDFs e fontes primárias (não versionar conteúdo sensível)
notas/        — notas técnicas e pareceres em markdown
pesquisas/    — levantamentos jurisprudenciais, doutrinários e patrimoniais
pipeline/     — módulos do pipeline cognitivo corporativo
```

## Documentos Principais

- [`pesquisas/whole-money-trail.md`](pesquisas/whole-money-trail.md) — rastreamento patrimonial completo
- [`pesquisas/mapa-ativos-penhoraveis.md`](pesquisas/mapa-ativos-penhoraveis.md) — ativos identificados e fundamentação
- [`notas/template-nota-tecnica.md`](notas/template-nota-tecnica.md) — modelo para notas técnicas e pareceres
