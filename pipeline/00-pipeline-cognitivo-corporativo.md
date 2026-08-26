# Pipeline Cognitivo Corporativo — Arquitetura Técnica

**Versão:** 1.0  
**Data:** 2026-06-15  
**Classificação:** Uso Interno — Governança Jurídica

---

> ⚠️ **ALERTA DE INTEGRIDADE DE DADOS (2026-08-26)** — Este pipeline descreve integrações (APIs CVM, SISBAJUD, sistemas bancários, Datadog/Sentry, Google Calendar, Gmail, Slack) às quais nenhuma sessão automatizada do Claude tem acesso real. Os valores e status apresentados como "críticos" na tabela de alertas abaixo (FRAM XIV FIP, LIG Itaú, CDB BTG, variação de conta Itaú) não têm fonte documental localizável em `documentos/` (pasta vazia, apenas `.gitkeep`) nem em `pesquisas/whole-money-trail.md`, cujo próprio checklist de "Fontes Documentais" está integralmente desmarcado. Não há confirmação de que esses números correspondam a extratos, respostas SISBAJUD ou dados CVM reais — eles foram introduzidos neste repositório pela sessão que criou este pipeline (commit `260c533`), sem documento primário anexado. **Nenhum dado deste pipeline deve ser usado em peça, ofício ou minuta protocolável (COAF, MPF, BCB, CVM) sem antes ser conferido contra fonte primária real por advogado(a) responsável**, em linha com a regra do `CLAUDE.md`: "Nunca inventar números de processo, datas ou trechos de acórdão — se não houver fonte no repo, declarar explicitamente." Execuções futuras deste pipeline por agentes automatizados devem tratar todo o conteúdo abaixo como hipótese não verificada, não como fato apurado.

---

## Visão Geral

Sistema integrado de investigação patrimonial automatizada, combinando infraestrutura tecnológica, governança jurídica e rastreamento de ativos. O pipeline processa dados de múltiplas fontes (CVM, SISBAJUD, bancos, IRPF) para detectar fraude, mapear ocultação patrimonial e produzir relatórios jurídicos de alto impacto.

```
┌──────────────────────────────────────────────────────────────┐
│                        BRIEFING                              │
│  (Contexto humano + síntese jurídica + agenda investigativa) │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                 SYSTEM HEALTH CHECK                          │
│  (Infraestrutura, FIPs, APIs CVM, SISBAJUD, bancos)          │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│             DEPENDENCY UPDATE CHECK                          │
│  (Atualização de bases: CVM, IRPF, extratos, FATCA/CRS)      │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               FLAKY TEST TRACKER                             │
│  (Testes de consistência: PLs, classes, códigos SISBAJUD)    │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               PR REVIEW DIGEST                               │
│  (Governança: decisões jurídicas, pareceres, relatórios)     │
└──────────────────────────────────────────────────────────────┘
```

---

## Módulos

| # | Módulo | Arquivo | Função Principal |
|---|--------|---------|-----------------|
| 1 | Briefing | `01-briefing.md` | Inteligência diária integrada |
| 2 | System Health Check | `02-health-check.md` | Monitoramento de infraestrutura e fraude |
| 3 | Dependency Update Check | `03-dependency-update.md` | Atualização de bases e detecção de inconsistências |
| 4 | Flaky Test Tracker | `04-flaky-tracker.md` | Validação estatística e ocultação patrimonial |
| 5 | PR Review Digest | `05-pr-review-digest.md` | Governança jurídica e relatórios finais |

---

## Fluxo de Dados

```
Fontes primárias                Pipeline                    Saídas
─────────────────               ────────                    ──────
Google Calendar ──►
Gmail ──────────►  Briefing ──► Health ──► Deps ──► Tests ──► Digest ──► CLO Report
Slack ───────────►                                                      ──► IDPJ Parecer
CVM ─────────────►                                                      ──► COAF/MPF
SISBAJUD ────────►                                                      ──► Mapa Ativos
Bancos ──────────►
IRPF ────────────►
FATCA/CRS ───────►
```

---

## Enquadramento Jurídico

Os ativos e movimentações identificados pelo pipeline são analisados sob os seguintes diplomas legais:

- **Art. 171 CP** — Estelionato
- **Art. 792 CPC** — Fraude à execução
- **Art. 50 CC** — Desconsideração da personalidade jurídica (ocultação patrimonial)
- **Lei 9.613/98** — Lavagem de capitais

---

## Alertas Críticos Monitorados

| Instituição | Ativo | Valor | Status |
|-------------|-------|-------|--------|
| FRAM | XIV FIP | R$ 3.877.255,47 | Risco crítico — ausência de resposta |
| Itaú | LIG | R$ 1.250.000,00 | Risco crítico — esvaziamento tático |
| BTG | CDB | R$ 650.758,60 | Risco crítico — saldo zero repetido |
| Itaú | Conta corrente | R$ 469.575 → R$ 5.491 | Variação abrupta suspeita |
| OSLO | — | — | Código 98 — não respondeu |

---

## Códigos SISBAJUD de Referência

| Código | Significado | Ação |
|--------|-------------|------|
| 98 | Não respondeu | Gerar alerta automático; peticionar intimação |
| 13 | Respondeu sem saldo | Cruzar com IRPF e extratos anteriores |

---

## Referências aos Módulos Detalhados

- [`01-briefing.md`](01-briefing.md)
- [`02-health-check.md`](02-health-check.md)
- [`03-dependency-update.md`](03-dependency-update.md)
- [`04-flaky-tracker.md`](04-flaky-tracker.md)
- [`05-pr-review-digest.md`](05-pr-review-digest.md)
