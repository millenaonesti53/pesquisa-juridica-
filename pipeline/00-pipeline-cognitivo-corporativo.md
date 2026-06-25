# Pipeline Cognitivo Corporativo — Diagrama Técnico (PhD TI)

**Versão:** 2.0  
**Data:** 2026-06-25  
**Classificação:** Uso Interno — Governança Jurídica  
**Integração:** Tecnologia · Governança Jurídica · Investigação Patrimonial

---

## Arquitetura do Pipeline

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

## Módulos — Índice

| # | Módulo | Arquivo | Função Principal |
|---|--------|---------|-----------------|
| 1 | 🌅 Briefing | [`01-briefing.md`](01-briefing.md) | Inteligência diária integrada |
| 2 | 🩺 System Health Check | [`02-health-check.md`](02-health-check.md) | Monitoramento de infraestrutura e fraude |
| 3 | 🔄 Dependency Update Check | [`03-dependency-update.md`](03-dependency-update.md) | Atualização de bases e detecção de inconsistências |
| 4 | 🧪 Flaky Test Tracker | [`04-flaky-tracker.md`](04-flaky-tracker.md) | Validação estatística e ocultação patrimonial |
| 5 | 🔍 PR Review Digest | [`05-pr-review-digest.md`](05-pr-review-digest.md) | Governança jurídica e relatórios finais |

---

## Rotinas Detalhadas por Módulo

### 🌅 1. Briefing — Rotina Técnica e Jurídica

**Função tecnológica**

- Agregar dados de múltiplas fontes (Google Calendar, Gmail, Slack, CVM, SISBAJUD)
- Gerar daily intelligence report

**Função jurídica**

Atualizar o CLO e o Núcleo de Governança sobre:
- Novos bloqueios
- Respostas bancárias
- Códigos SISBAJUD
- Movimentações suspeitas
- Atualizações de FIPs

**Rotina integrada**

1. Carrega o Whole Money Trail do dia anterior
2. Atualiza o status das instituições:
   - Código 98 (não respondeu)
   - Código 13 (respondeu sem saldo)
3. Gera alerta automático para:
   - FRAM / OSLO (não resposta)
   - BTG / Itaú (esvaziamento tático)

---

### 🩺 2. System Health Check — Rotina Técnica e Jurídica

**Função tecnológica**

Monitorar:
- APIs CVM
- Datadog / Sentry
- Bancos
- Integradores SISBAJUD

**Função jurídica**

Verificar:
- Inconsistências de PL
- Divergências entre IRPF × CVM
- Ausência de resposta (cód. 98)
- Sinais de ocultação patrimonial

**Rotina integrada**

Detecta:
- FRAM XIV FIP → R$ 3.877.255,47
- LIG Itaú → R$ 1.250.000,00
- CDB BTG → R$ 650.758,60

Marca como risco crítico:
- Instituições que não respondem
- Contas com variação abrupta (ex.: Itaú R$ 469.575 → R$ 5.491)

---

### 🔄 3. Dependency Update Check — Rotina Técnica e Jurídica

**Função tecnológica**

Atualizar:
- Bases CVM
- Extratos
- IRPF
- Logs FATCA/CRS
- Dados de FIPs

**Função jurídica**

Verificar:
- Criação retroativa de classes (ex.: Classe J)
- Side-pockets
- Alterações de regulamento
- Cisões e SPVs novas

**Rotina integrada**

Detecta:
- Bonifácio FIP criado pós-litígio
- Side-pocket no FRAM
- Inconsistência temporal no Ajaccio

---

### 🧪 4. Flaky Test Tracker — Rotina Técnica e Jurídica

**Função tecnológica**

Identificar inconsistências estatísticas:
- PLs variando sem justificativa
- Respostas bancárias incoerentes
- Divergências entre fontes

**Função jurídica**

Testar:
- Se a alegação de iliquidez é consistente
- Se há padrão de esvaziamento pré-ordem
- Se há ocultação sistemática

**Rotina integrada**

Marca como flaky:
- BTG → saldo zero repetido com movimentação prévia
- Itaú → esvaziamento tático
- FRAM / OSLO → ausência de resposta

---

### 🔍 5. PR Review Digest — Rotina Técnica e Jurídica

**Função tecnológica**

Consolidar:
- Relatórios
- Pareceres
- Análises
- Decisões pendentes

**Função jurídica**

Revisar:
- Enquadramento penal (art. 171 CP)
- Fraude à execução (CPC 792)
- Ocultação patrimonial (CC 50)
- Lavagem (Lei 9.613/98)

**Rotina integrada**

Gera:
- Relatório final para CLO
- Parecer para IDPJ
- Minuta para COAF/MPF
- Mapa de ativos penhoráveis

---

## Fluxo de Dados

```
Fontes primárias                Pipeline                     Saídas
─────────────────               ────────                     ──────
Google Calendar ──►
Gmail ──────────►  Briefing ──► Health ──► Deps ──► Tests ──► Digest ──► CLO Report
Slack ───────────►                                                       ──► IDPJ Parecer
CVM ─────────────►                                                       ──► COAF/MPF
SISBAJUD ────────►                                                       ──► Mapa Ativos
Bancos ──────────►
IRPF ────────────►
FATCA/CRS ───────►
```

---

## Enquadramento Jurídico

| Diploma | Dispositivo | Conduta Identificada |
|---------|-------------|---------------------|
| Código Penal | Art. 171 | Estelionato |
| CPC | Art. 792 | Fraude à execução |
| Código Civil | Art. 50 | Ocultação via abuso de personalidade jurídica |
| Lei 9.613/98 | Arts. 1°-2° | Lavagem de capitais |
| CPC | Art. 774 | Atos atentatórios à dignidade da justiça |
| CPC | Art. 835, IX | Penhorabilidade de cotas de fundos |

---

## Alertas Críticos Ativos

| Instituição | Ativo | Valor | Status |
|-------------|-------|-------|--------|
| FRAM | XIV FIP | R$ 3.877.255,47 | Risco crítico — ausência de resposta (cód. 98) |
| Itaú | LIG | R$ 1.250.000,00 | Risco crítico — esvaziamento tático |
| BTG | CDB | R$ 650.758,60 | Risco crítico — saldo zero repetido |
| Itaú | Conta corrente | R$ 469.575 → R$ 5.491 | Variação abrupta suspeita (-98,8%) |
| OSLO | — | A apurar | Código 98 — não respondeu |

---

## Códigos SISBAJUD de Referência

| Código | Significado | Ação no Pipeline |
|--------|-------------|-----------------|
| 98 | Não respondeu | Alerta crítico; peticionar intimação; representar ao BCB |
| 13 | Respondeu sem saldo | Cruzar com IRPF, extratos anteriores e CVM |

---

## Conclusão — Sistema de Investigação Patrimonial Automatizada

Cada módulo alimenta o próximo:

1. **Briefing** → contexto humano + jurídico
2. **Health Check** → estabilidade técnica + detecção de fraude
3. **Dependency Check** → atualização de dados + inconsistências
4. **Flaky Tracker** → validação estatística + ocultação
5. **PR Digest** → governança + decisões jurídicas

O resultado é um sistema integrado de investigação patrimonial capaz de:

- Detectar fraude
- Mapear ocultação
- Identificar ativos penhoráveis
- Desmontar alegações de impenhorabilidade
- Reconstruir o Whole Money Trail
- Produzir relatórios jurídicos de alto impacto para CLO, IDPJ, COAF e MPF
