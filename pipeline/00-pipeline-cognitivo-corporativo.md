# Pipeline Cognitivo Corporativo — Arquitetura Técnica

**Versão:** 3.0  
**Data:** 2026-06-20  
**Classificação:** Uso Interno — Governança Jurídica  
**Nível técnico:** PhD TI — Integração Tecnologia + Governança Jurídica + Investigação Patrimonial

---

## Visão Geral

Sistema integrado de investigação patrimonial automatizada, combinando infraestrutura tecnológica, governança jurídica e rastreamento de ativos. O pipeline processa dados de múltiplas fontes (CVM, SISBAJUD, bancos, IRPF) para detectar fraude, mapear ocultação patrimonial e produzir relatórios jurídicos de alto impacto.

```
┌──────────────────────────────────────────────────────────────┐
│                     🌅 BRIEFING                              │
│  (Contexto humano + síntese jurídica + agenda investigativa) │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                 🩺 SYSTEM HEALTH CHECK                        │
│  (Infraestrutura, FIPs, APIs CVM, SISBAJUD, bancos)          │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│             🔄 DEPENDENCY UPDATE CHECK                        │
│  (Atualização de bases: CVM, IRPF, extratos, FATCA/CRS)      │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               🧪 FLAKY TEST TRACKER                           │
│  (Testes de consistência: PLs, classes, códigos SISBAJUD)    │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               🔍 PR REVIEW DIGEST                             │
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

## Rotinas Integradas por Módulo

### 🌅 1. Briefing — Rotina Técnica e Jurídica

**Função tecnológica:** Agregar dados de múltiplas fontes (Google Calendar, Gmail, Slack, CVM, SISBAJUD) e gerar daily intelligence report.

**Função jurídica:** Atualizar o CLO e o Núcleo de Governança sobre novos bloqueios, respostas bancárias, códigos SISBAJUD, movimentações suspeitas e atualizações de FIPs.

**Rotina integrada:**
- Carrega o Whole Money Trail do dia anterior
- Atualiza o status das instituições: Código 98 (não respondeu) / Código 13 (respondeu sem saldo)
- Gera alerta automático para FRAM/OSLO (não resposta) e BTG/Itaú (esvaziamento tático)

---

### 🩺 2. System Health Check — Rotina Técnica e Jurídica

**Função tecnológica:** Monitorar APIs CVM, Datadog, Sentry, bancos e integradores SISBAJUD.

**Função jurídica:** Verificar inconsistências de PL, divergências entre IRPF × CVM, ausência de resposta (cód. 98) e sinais de ocultação patrimonial.

**Rotina integrada:**
- Detecta: FRAM XIV FIP → R$ 3.877.255,47 | LIG Itaú → R$ 1.250.000,00 | CDB BTG → R$ 650.758,60
- Marca como risco crítico: instituições que não respondem; contas com variação abrupta (Itaú: R$ 469.575 → R$ 5.491)

---

### 🔄 3. Dependency Update Check — Rotina Técnica e Jurídica

**Função tecnológica:** Atualizar bases CVM, extratos, IRPF, logs FATCA/CRS e dados de FIPs.

**Função jurídica:** Verificar criação retroativa de classes (ex.: Classe J), side-pockets, alterações de regulamento, cisões e SPVs novas.

**Rotina integrada:**
- Detecta: Bonifácio FIP criado pós-litígio; side-pocket no FRAM; inconsistência temporal no Ajaccio

---

### 🧪 4. Flaky Test Tracker — Rotina Técnica e Jurídica

**Função tecnológica:** Identificar inconsistências estatísticas — PLs variando sem justificativa, respostas bancárias incoerentes, divergências entre fontes.

**Função jurídica:** Testar se a alegação de iliquidez é consistente; se há padrão de esvaziamento pré-ordem; se há ocultação sistemática.

**Rotina integrada:**
- Marca como flaky: BTG → saldo zero repetido com movimentação prévia; Itaú → esvaziamento tático; FRAM/OSLO → ausência de resposta sistemática

---

### 🔍 5. PR Review Digest — Rotina Técnica e Jurídica

**Função tecnológica:** Consolidar relatórios, pareceres, análises e decisões pendentes.

**Função jurídica:** Revisar enquadramento penal (art. 171 CP), fraude à execução (CPC 792), ocultação patrimonial (CC 50) e lavagem (Lei 9.613/98).

**Rotina integrada:**
- Gera: relatório final para CLO; parecer para IDPJ; minuta para COAF/MPF; mapa de ativos penhoráveis

---

## Resultado Final do Pipeline

O pipeline produz um sistema de investigação patrimonial automatizado capaz de:

1. Detectar fraude patrimonial (padrões estatísticos + temporais)
2. Mapear ocultação (FIPs, SPVs, contas offshore, FATCA/CRS)
3. Identificar ativos penhoráveis (cotas, CDBs, LIGs, imóveis)
4. Desmontar alegações de impenhorabilidade (iliquidez, FAPI, previdência)
5. Reconstruir o Whole Money Trail (origem → veículos → beneficiários)
6. Produzir relatórios jurídicos de alto impacto (CLO, COAF, MPF, IDPJ)

---

## Registro de Execuções

| Data | Briefing | Alertas Críticos | Total Identificado | Branch |
|------|----------|------------------|--------------------|--------|
| 2026-06-20 | [briefing-2026-06-20.md](../notas/briefing-2026-06-20.md) | 5 | R$ 5.783.505,07 + a apurar | claude/friendly-goldberg-xeajez |
| 2026-06-19 | briefing-2026-06-19.md | 5 | R$ 5.778.014,07 + a apurar | claude/friendly-goldberg-02mvd4 |
| 2026-06-18 | briefing-2026-06-18.md | 5 | R$ 5.778.014,07 | claude/friendly-goldberg-gc3675 |

---

## Referências aos Módulos Detalhados

- [`01-briefing.md`](01-briefing.md)
- [`02-health-check.md`](02-health-check.md)
- [`03-dependency-update.md`](03-dependency-update.md)
- [`04-flaky-tracker.md`](04-flaky-tracker.md)
- [`05-pr-review-digest.md`](05-pr-review-digest.md)
