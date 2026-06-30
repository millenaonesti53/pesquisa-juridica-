# Pipeline Cognitivo Corporativo — Diagrama Técnico (PhD TI)

**Integração entre Tecnologia, Governança Jurídica e Investigação Patrimonial**  
**Versão:** 2.0  
**Data:** 2026-06-30  
**Classificação:** Uso Interno — Governança Jurídica

---

## Arquitetura do Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                        🌅 BRIEFING                           │
│  (Contexto humano + síntese jurídica + agenda investigativa) │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                 🩺 SYSTEM HEALTH CHECK                        │
│  (Infraestrutura, FIPs, APIs CVM, SISBAJUD, bancos)           │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│             🔄 DEPENDENCY UPDATE CHECK                        │
│  (Atualização de bases: CVM, IRPF, extratos, FATCA/CRS)       │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               🧪 FLAKY TEST TRACKER                           │
│  (Testes de consistência: PLs, classes, códigos SISBAJUD)     │
└───────────────┬──────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│               🔍 PR REVIEW DIGEST                             │
│  (Governança: decisões jurídicas, pareceres, relatórios)      │
└──────────────────────────────────────────────────────────────┘
```

---

## Módulos

| # | Módulo | Arquivo | Função Principal |
|---|--------|---------|-----------------|
| 1 | 🌅 Briefing | `01-briefing.md` | Inteligência diária integrada |
| 2 | 🩺 System Health Check | `02-health-check.md` | Monitoramento de infraestrutura e fraude |
| 3 | 🔄 Dependency Update Check | `03-dependency-update.md` | Atualização de bases e detecção de inconsistências |
| 4 | 🧪 Flaky Test Tracker | `04-flaky-tracker.md` | Validação estatística e ocultação patrimonial |
| 5 | 🔍 PR Review Digest | `05-pr-review-digest.md` | Governança jurídica e relatórios finais |

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

## Rotinas Integradas por Módulo

### 🌅 1. BRIEFING — Rotina Técnica e Jurídica

**Função tecnológica**
- Agregar dados de múltiplas fontes (Google Calendar, Gmail, Slack, CVM, SISBAJUD)
- Gerar daily intelligence report

**Função jurídica**  
Atualizar o CLO e o Núcleo de Governança sobre:
- novos bloqueios
- respostas bancárias e códigos SISBAJUD
- movimentações suspeitas
- atualizações de FIPs

**Rotina integrada**
1. Carregar o Whole Money Trail do dia anterior
2. Atualizar status das instituições:
   - Código 98 (não respondeu)
   - Código 13 (respondeu sem saldo)
3. Gerar alerta automático para:
   - FRAM / OSLO — não resposta
   - BTG / Itaú — esvaziamento tático

---

### 🩺 2. SYSTEM HEALTH CHECK — Rotina Técnica e Jurídica

**Função tecnológica**  
Monitorar: APIs CVM, Datadog, Sentry, bancos, integradores SISBAJUD

**Função jurídica**  
Verificar:
- inconsistências de PL
- divergências entre IRPF × CVM
- ausência de resposta (cód. 98)
- sinais de ocultação patrimonial

**Rotina integrada — Ativos monitorados**

| Ativo | Instituição | Valor | Status |
|-------|-------------|-------|--------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Risco crítico |
| LIG | Itaú | R$ 1.250.000,00 | Risco crítico |
| CDB | BTG | R$ 650.758,60 | Risco crítico |
| Conta corrente | Itaú | R$ 469.575 → R$ 5.491 | Variação abrupta suspeita |

---

### 🔄 3. DEPENDENCY UPDATE CHECK — Rotina Técnica e Jurídica

**Função tecnológica**  
Atualizar: bases CVM, extratos, IRPF, logs FATCA/CRS, dados de FIPs

**Função jurídica**  
Verificar:
- criação retroativa de classes (ex.: Classe J)
- side-pockets
- alterações de regulamento
- cisões e SPVs novas

**Rotina integrada — Casos detectados**
- Bonifácio FIP criado pós-litígio
- Side-pocket no FRAM
- Inconsistência temporal no Ajaccio

---

### 🧪 4. FLAKY TEST TRACKER — Rotina Técnica e Jurídica

**Função tecnológica**  
Identificar inconsistências estatísticas:
- PLs variando sem justificativa
- respostas bancárias incoerentes
- divergências entre fontes

**Função jurídica**  
Testar:
- se a alegação de iliquidez é consistente
- se há padrão de esvaziamento pré-ordem
- se há ocultação sistemática

**Rotina integrada — Casos marcados como flaky**

| Instituição | Padrão | Classificação |
|-------------|--------|---------------|
| BTG | Saldo zero repetido com movimentação prévia | FLAKY |
| Itaú | Esvaziamento tático (-98,8%) | FLAKY |
| FRAM | Ausência de resposta sistemática (cód. 98) | FLAKY |
| OSLO | Ausência de resposta sistemática (cód. 98) | FLAKY |

---

### 🔍 5. PR REVIEW DIGEST — Rotina Técnica e Jurídica

**Função tecnológica**  
Consolidar: relatórios, pareceres, análises, decisões pendentes

**Função jurídica**  
Revisar enquadramento:

| Diploma | Dispositivo | Conduta |
|---------|-------------|---------|
| Código Penal | Art. 171 | Estelionato |
| CPC | Art. 792 | Fraude à execução |
| Código Civil | Art. 50 | Ocultação patrimonial (DPJ) |
| Lei 9.613/98 | Arts. 1°–2° | Lavagem de capitais |

**Rotina integrada — Documentos gerados**
- Relatório final para CLO
- Parecer para IDPJ
- Minuta para COAF/MPF
- Mapa de ativos penhoráveis

---

## Códigos SISBAJUD de Referência

| Código | Significado | Ação |
|--------|-------------|------|
| 98 | Não respondeu | Gerar alerta; peticionar intimação |
| 13 | Respondeu sem saldo | Cruzar com IRPF e extratos anteriores |

---

## Conclusão — Capacidades do Sistema

O pipeline entrega um sistema de investigação patrimonial automatizado, capaz de:

1. **Detectar fraude** — por cruzamento de fontes heterogêneas
2. **Mapear ocultação** — por análise estatística de inconsistências
3. **Identificar ativos penhoráveis** — por rastreamento do whole money trail
4. **Desmontar alegações de impenhorabilidade** — por evidências documentais
5. **Reconstruir o whole money trail** — da origem ao veículo final de ocultação
6. **Produzir relatórios jurídicos de alto impacto** — estruturados para CLO, IDPJ, COAF e MPF

---

## Referências aos Módulos Detalhados

- [`01-briefing.md`](01-briefing.md)
- [`02-health-check.md`](02-health-check.md)
- [`03-dependency-update.md`](03-dependency-update.md)
- [`04-flaky-tracker.md`](04-flaky-tracker.md)
- [`05-pr-review-digest.md`](05-pr-review-digest.md)
