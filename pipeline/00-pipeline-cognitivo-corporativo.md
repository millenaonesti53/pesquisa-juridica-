# Pipeline Cognitivo Corporativo — Arquitetura Técnica (PhD TI)

**Versão:** 2.0  
**Data:** 2026-06-19  
**Classificação:** Uso Interno — Governança Jurídica  
**Integração:** Tecnologia · Governança Jurídica · Investigação Patrimonial

---

## Diagrama de Fluxo

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
Fontes primárias                Pipeline                         Saídas
─────────────────               ────────                         ──────
Google Calendar ──►
Gmail ──────────►  BRIEFING ──► HEALTH ──► DEPS ──► TESTS ──► DIGEST ──► CLO Report
Slack ───────────►                                                       ──► IDPJ Parecer
CVM ─────────────►                                                       ──► COAF/MPF
SISBAJUD ────────►                                                       ──► Mapa Ativos
Bancos ──────────►
IRPF ────────────►
FATCA/CRS ───────►
```

---

## Rotinas Detalhadas por Módulo

### Módulo 1 — Briefing: Rotina Técnica e Jurídica

**Função tecnológica**
- Agrega dados de Google Calendar, Gmail, Slack, CVM e SISBAJUD
- Gera daily intelligence report consolidado

**Função jurídica**
- Atualiza CLO e Núcleo de Governança sobre:
  - Novos bloqueios determinados
  - Respostas bancárias e códigos SISBAJUD
  - Movimentações suspeitas no período
  - Atualizações de FIPs

**Rotina integrada**
1. Carrega o Whole Money Trail do dia anterior
2. Atualiza status das instituições por código SISBAJUD
3. Gera alerta automático para:
   - FRAM / OSLO → código 98 (não respondeu)
   - BTG / Itaú → esvaziamento tático

---

### Módulo 2 — System Health Check: Rotina Técnica e Jurídica

**Função tecnológica**
- Monitora: APIs CVM, Datadog, Sentry, bancos, integradores SISBAJUD

**Função jurídica**
- Verifica:
  - Inconsistências de PL (Patrimônio Líquido declarado vs. calculado)
  - Divergências IRPF × CVM
  - Ausência de resposta como possível obstrução (cód. 98)
  - Sinais de ocultação patrimonial

**Ativos detectados e monitorados**

| Ativo | Instituição | PL Registrado | Status | Risco |
|-------|-------------|---------------|--------|-------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Sem resposta (cód. 98) | CRÍTICO |
| LIG | Itaú | R$ 1.250.000,00 | Esvaziamento tático | CRÍTICO |
| CDB | BTG | R$ 650.758,60 | Saldo zero repetido | ALTO |
| Conta corrente | Itaú | R$ 469.575 → R$ 5.491 | Variação abrupta | ALTO |

---

### Módulo 3 — Dependency Update Check: Rotina Técnica e Jurídica

**Função tecnológica**
- Atualiza: bases CVM, extratos, IRPF, logs FATCA/CRS, dados de FIPs

**Função jurídica**
- Verifica:
  - Criação retroativa de classes (ex.: Classe J criada pós-litígio)
  - Side-pockets e segregação de ativos
  - Alterações de regulamento que dificultem a penhora
  - Cisões e SPVs novas constituídas após ajuizamento

**Casos detectados**
- **Bonifácio FIP** — criado pós-litígio → enquadramento art. 792, IV, CPC
- **FRAM XIV** — side-pocket suspeito → iliquidez alegada vs. PL real R$ 3.877.255,47
- **Ajaccio** — inconsistência temporal → possível simulação (art. 167 CC)

---

### Módulo 4 — Flaky Test Tracker: Rotina Técnica e Jurídica

**Função tecnológica**
- Identifica inconsistências estatísticas:
  - PLs variando sem justificativa econômica documentada
  - Respostas bancárias incoerentes entre si ou com o histórico
  - Divergências entre fontes primárias independentes

**Função jurídica**
- Testa:
  - Se a alegação de iliquidez é sustentável (FIPs)
  - Se há padrão temporal de esvaziamento pré-ordem
  - Se há ocultação sistêmica (múltiplas instituições, mesmo padrão)

**Casos marcados como flaky**

| Instituição | Tipo | Classificação |
|-------------|------|--------------|
| BTG | Saldo zero repetido com histórico positivo | FLAKY — resposta inconsistente |
| Itaú | Variação -98,8% pós-intimação | FLAKY — esvaziamento tático |
| FRAM | Código 98 sistemático | FLAKY — não resposta coordenada |
| OSLO | Código 98 sistemático | FLAKY — não resposta coordenada |

---

### Módulo 5 — PR Review Digest: Rotina Técnica e Jurídica

**Função tecnológica**
- Consolida relatórios, pareceres, análises e decisões pendentes em documentos estruturados

**Função jurídica**
- Revisão de enquadramento:
  - Art. 171 CP — Estelionato
  - Art. 792 CPC — Fraude à execução
  - Art. 50 CC — Ocultação patrimonial via abuso da personalidade jurídica
  - Lei 9.613/98 — Lavagem de capitais

**Documentos gerados por ciclo**
- `notas/relatorio-clo-[data].md` — relatório executivo para CLO
- `notas/parecer-idpj-[data].md` — parecer estruturado para IDPJ
- `notas/minuta-coaf-[data].md` — minuta para COAF / MPF
- `pesquisas/mapa-ativos-penhoraveis.md` — mapa atualizado de ativos

---

## Alertas Críticos Ativos

| Instituição | Ativo | Valor | Código SISBAJUD | Status |
|-------------|-------|-------|-----------------|--------|
| FRAM | XIV FIP | R$ 3.877.255,47 | 98 | Risco crítico — ausência de resposta |
| Itaú | LIG | R$ 1.250.000,00 | — | Risco crítico — esvaziamento tático |
| BTG | CDB | R$ 650.758,60 | 13 | Risco alto — saldo zero repetido |
| Itaú | Conta corrente | R$ 469.575 → R$ 5.491 | — | Variação abrupta -98,8% |
| OSLO | — | A apurar | 98 | Código 98 — não respondeu |

---

## Códigos SISBAJUD de Referência

| Código | Significado | Ação |
|--------|-------------|------|
| 98 | Não respondeu | Alerta automático; peticionar intimação; representar ao BCB |
| 13 | Respondeu sem saldo | Cruzar com IRPF e extratos anteriores; avaliar flakiness |

---

## Enquadramento Jurídico

| Diploma | Dispositivo | Conduta |
|---------|-------------|---------|
| Código Penal | Art. 171 | Estelionato |
| CPC | Art. 792 | Fraude à execução |
| Código Civil | Art. 50 | Desconsideração da personalidade jurídica |
| Lei 9.613/98 | Arts. 1°-2° | Lavagem de capitais |
| CPC | Art. 774 | Atos atentatórios à dignidade da justiça |
| CPC | Art. 835, IX | Penhorabilidade de cotas de fundos |

---

## Resultado Final do Pipeline

O sistema produz, por ciclo de execução:

1. **Detecção de fraude** — padrões estatísticos e inconsistências documentais
2. **Mapeamento de ocultação** — veículos patrimoniais, side-pockets, SPVs
3. **Identificação de ativos penhoráveis** — com fundamentação jurídica
4. **Desmonte de alegações de impenhorabilidade** — FIPs, LIGs e equivalentes
5. **Reconstrução do Whole Money Trail** — origem → veículos → beneficiários finais
6. **Relatórios jurídicos de alto impacto** — CLO, IDPJ, COAF, MPF

---

## Referências aos Módulos

- [`01-briefing.md`](01-briefing.md)
- [`02-health-check.md`](02-health-check.md)
- [`03-dependency-update.md`](03-dependency-update.md)
- [`04-flaky-tracker.md`](04-flaky-tracker.md)
- [`05-pr-review-digest.md`](05-pr-review-digest.md)
- [`../pesquisas/whole-money-trail.md`](../pesquisas/whole-money-trail.md)
- [`../pesquisas/mapa-ativos-penhoraveis.md`](../pesquisas/mapa-ativos-penhoraveis.md)
