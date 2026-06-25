# Módulo 2 — 🩺 System Health Check

**Pipeline Cognitivo Corporativo | Estágio 2/5 | v2.0**

---

## Visão Geral

Verifica a integridade das fontes de dados e detecta sinais técnicos de manipulação ou ocultação patrimonial. Alimenta o pipeline com um mapa de inconsistências jurídico-financeiras.

---

## Função Tecnológica

Monitorar disponibilidade e integridade das integrações:

| Sistema | O que monitora | Ferramenta |
|---------|---------------|-----------|
| APIs CVM | Disponibilidade, latência, dados de FIPs | Request + healthcheck |
| Datadog / Sentry | Logs de erro, anomalias, alertas | Dashboard |
| Conectores SISBAJUD | Tempo de resposta, falhas de comunicação | Log parser |
| Sistemas bancários | Status de bloqueios, respostas recebidas | SISBAJUD integrado |

---

## Função Jurídica

Verificar sinais de manipulação ou ocultação patrimonial:

1. **Inconsistências de PL** — Patrimônio Líquido declarado vs. calculado
2. **Divergências IRPF × CVM** — bens declarados à Receita vs. registros CVM
3. **Ausência de resposta sistemática** — cód. 98 como possível obstrução deliberada
4. **Sinais de ocultação patrimonial** — movimentações abruptas sem lastro documental

---

## Rotina Integrada

### Ativos sob Monitoramento Ativo

| Ativo | Instituição | PL Registrado | Status | Risco |
|-------|-------------|---------------|--------|-------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Sem resposta (cód. 98) | **CRÍTICO** |
| LIG | Itaú | R$ 1.250.000,00 | Esvaziamento tático pós-intimação | **CRÍTICO** |
| CDB | BTG | R$ 650.758,60 | Saldo zero repetido | **ALTO** |
| Conta corrente | Itaú | R$ 469.575 → R$ 5.491 | Variação -98,8% | **ALTO** |

### Verificações de Consistência

```
Para cada FIP monitorado:
  1. Comparar PL atual × PL última declaração CVM
  2. Verificar se há side-pockets não declarados
  3. Checar se houve alteração de regulamento sem notificação
  4. Identificar novas classes de cotas criadas pós-litígio
  5. Verificar emissão/resgate de cotas após ordem de bloqueio

Para cada conta bancária:
  1. Comparar saldo SISBAJUD × extrato fornecido voluntariamente
  2. Verificar movimentações nos 30 dias anteriores à ordem de bloqueio
  3. Calcular variação percentual e classificar risco
  4. Cruzar com IRPF — verificar divergências
```

### Matriz de Risco

| Indicador | Normal | Atenção | Crítico |
|-----------|--------|---------|---------|
| Variação de saldo | < 20% | 20–50% | > 50% |
| Dias sem resposta (cód. 98) | 0 | 1–5 | > 5 |
| Divergência IRPF × CVM | R$ 0 | até R$ 50k | > R$ 50k |
| Novas classes pós-litígio | Não | — | Sim |
| Side-pocket identificado | Não | — | Sim |

---

## Caso Documentado — Itaú: Esvaziamento Tático

| Momento | Saldo | Variação | Evento |
|---------|-------|----------|--------|
| Pré-intimação (T-1) | R$ 469.575,00 | — | Saldo normal |
| Pós-intimação (T0) | R$ 5.491,00 | **-98,8%** | Após recebimento da ordem |

**Enquadramento:** fraude à execução (art. 792 CPC) + ocultação patrimonial (art. 50 CC).

**Ação:** requerer extratos detalhados do período T-30 a T+30; identificar destinatários; peticionar bloqueio nas contas de destino.

---

## Caso Documentado — FRAM / OSLO: Não Resposta Sistemática

| Instituição | Código | Ativo Relacionado | Ocorrências |
|-------------|--------|-------------------|------------|
| FRAM | 98 | XIV FIP (R$ 3.877.255,47) | Múltiplas ordens |
| OSLO | 98 | A apurar | Múltiplas ordens |

**Hipótese:** coordenação entre as entidades para obstruir a execução.

**Enquadramento:** art. 774 CPC (ato atentatório à dignidade da justiça); Lei 4.595/64 (competência do BCB para supervisão).

**Ação:** peticionar multa; requerer intimação pessoal dos administradores; representar ao BCB e à CVM.

---

## Saída do Módulo

- Relatório de saúde do sistema (técnico) → log interno
- **Mapa de inconsistências jurídicas** → alimenta Módulo 3 (Dependency Update)
- Alertas críticos → redistribuídos ao Briefing do dia seguinte

---

## Legislação de Referência

- Art. 50, CC — Desconsideração da personalidade jurídica
- Art. 167, CC — Simulação (invalidade de negócio simulado)
- Art. 774, CPC — Atos atentatórios à dignidade da justiça
- Art. 792, CPC — Fraude à execução
- Lei 4.595/64 — Competência do BCB
- Lei 9.613/98, Art. 1° — Lavagem de capitais
