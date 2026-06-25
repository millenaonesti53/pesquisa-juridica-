# Módulo 1 — 🌅 Briefing

**Pipeline Cognitivo Corporativo | Estágio 1/5 | v2.0**

---

## Visão Geral

Agrega dados de múltiplas fontes para gerar o **daily intelligence report** consolidado e distribuí-lo ao CLO e ao Núcleo de Governança antes do início das atividades do dia.

---

## Função Tecnológica

Fontes integradas:

| Fonte | Dado Coletado | Periodicidade |
|-------|--------------|--------------|
| Google Calendar | Audiências, prazos processuais, reuniões | Diária |
| Gmail | Respostas bancárias, ofícios, decisões judiciais | Diária |
| Slack | Comunicações internas do Núcleo de Governança | Diária |
| CVM | Atualizações de FIPs, regulamentos, PLs | Diária |
| SISBAJUD | Ordens de bloqueio, respostas e códigos | Diária |

---

## Função Jurídica

Atualizar o CLO e o Núcleo de Governança sobre:

1. **Novos bloqueios** determinados pelo juízo
2. **Respostas bancárias** recebidas com seus códigos SISBAJUD
3. **Códigos SISBAJUD** — interpretação e ação imediata
4. **Movimentações suspeitas** identificadas no período
5. **Atualizações de FIPs** (alterações de regulamento, PL, classes de cotas)

---

## Rotina Integrada

### Entrada
- Whole Money Trail do dia anterior (atualizado)
- Status das respostas bancárias pendentes
- Log de eventos do SISBAJUD nas últimas 24h

### Processamento

```
Para cada instituição monitorada:
  1. Verificar código SISBAJUD mais recente
  2. Comparar saldo atual × histórico
  3. Classificar risco: normal / atenção / crítico
  4. Gerar alerta automático se:
     - Código 98 (não respondeu)
     - Código 13 com histórico de saldo positivo
     - Variação > 50% sem justificativa registrada

Para cada FIP monitorado:
  1. Verificar PL atual × PL anterior
  2. Verificar se houve alteração de regulamento
  3. Verificar emissão/resgate de cotas no período
```

### Alertas Automáticos — Gatilhos Ativos

| Instituição | Ativo | Gatilho | Prioridade |
|-------------|-------|---------|------------|
| FRAM | XIV FIP | Não resposta (cód. 98) | **CRÍTICA** |
| OSLO | — | Não resposta (cód. 98) | **CRÍTICA** |
| BTG | CDB | Esvaziamento tático (saldo zero repetido) | **ALTA** |
| Itaú | LIG + conta | Esvaziamento tático (R$ 469.575 → R$ 5.491) | **ALTA** |

### Saída
- Relatório de inteligência diária → `notas/briefing-AAAA-MM-DD.md`
- Lista de pendências para o Módulo 2 (Health Check)
- Alertas distribuídos via Slack / Gmail para o Núcleo de Governança

---

## Template de Saída — Briefing Diário

```markdown
# Briefing Diário — [DATA]

**Classificação:** Confidencial — uso interno

## Resumo Executivo
[2-3 frases sobre o estado geral da investigação]

## Novos Eventos
- [ ] [Evento 1 — tipo: bloqueio / resposta / decisão]
- [ ] [Evento 2]

## Status SISBAJUD
| Instituição | Ativo | Código | Saldo Reportado | Variação | Risco |
|-------------|-------|--------|-----------------|----------|-------|
| FRAM | XIV FIP | 98 | — | — | CRÍTICO |
| OSLO | — | 98 | — | — | CRÍTICO |
| BTG | CDB | 13 | R$ 0,00 | -100% | ALTO |
| Itaú | Conta | — | R$ 5.491,00 | -98,8% | ALTO |

## Alertas Ativos
- [ ] [Alerta 1 — ação requerida]
- [ ] [Alerta 2]

## Próximos Passos
- [ ] [Ação para hoje]
- [ ] [Ação para esta semana]
```

---

## Legislação de Referência

- Art. 774, CPC — Atos atentatórios à dignidade da justiça (descumprimento de ordens)
- Art. 792, IV, CPC — Fraude à execução (alienação pós-citação)
- Lei 4.595/64 — Competência do BCB para supervisionar instituições financeiras
