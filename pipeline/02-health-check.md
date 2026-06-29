# Módulo 2 — System Health Check

**Pipeline Cognitivo Corporativo | Estágio 2/5**

---

## Função Tecnológica

Monitorar a disponibilidade e integridade das fontes de dados:

- APIs CVM (Comissão de Valores Mobiliários)
- Datadog / Sentry — logs de erro e anomalias
- Conectores SISBAJUD — tempo de resposta e falhas
- Sistemas bancários integrados

## Função Jurídica

Verificar sinais de manipulação ou ocultação patrimonial:

1. **Inconsistências de PL** — Patrimônio Líquido declarado vs. calculado
2. **Divergências IRPF × CVM** — bens declarados à Receita vs. registros CVM
3. **Ausência de resposta** — código 98 como possível obstrução intencional
4. **Sinais de ocultação** — movimentações abruptas sem lastro documental

## Rotina Integrada

### Ativos Detectados sob Monitoramento Ativo

| Ativo | Instituição | PL Registrado | Status | Risco |
|-------|-------------|---------------|--------|-------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Sem resposta (cód. 98) | CRÍTICO |
| LIG | Itaú | R$ 1.250.000,00 | Esvaziamento tático | CRÍTICO |
| CDB | BTG | R$ 650.758,60 | Saldo zero repetido | ALTO |

### Marcação como Risco Crítico

O sistema marca como risco crítico:

- Instituições que não respondem às ordens SISBAJUD
- Contas com variação abrupta inexplicada (ex.: Itaú R$ 469.575 → R$ 5.491)

### Verificações de Consistência

```
Para cada FIP monitorado:
  1. Comparar PL atual × PL última declaração CVM
  2. Verificar se há side-pockets não declarados
  3. Checar se houve alteração de regulamento sem notificação
  4. Identificar novas classes de cotas criadas pós-litígio

Para cada conta bancária:
  1. Comparar saldo SISBAJUD × extrato fornecido voluntariamente
  2. Verificar movimentações nos 30 dias anteriores à ordem de bloqueio
  3. Calcular variação percentual e classificar risco
```

### Matriz de Risco

| Indicador | Limiar Normal | Limiar Atenção | Limiar Crítico |
|-----------|--------------|----------------|----------------|
| Variação de saldo | < 20% | 20–50% | > 50% |
| Dias sem resposta (cód. 98) | 0 | 1–5 | > 5 |
| Divergência IRPF × CVM | R$ 0 | até R$ 50k | > R$ 50k |
| Novas classes pós-litígio | Não | — | Sim |

### Caso Itaú — Documentação de Esvaziamento

| Data | Saldo | Variação | Evento |
|------|-------|----------|--------|
| [T-1] | R$ 469.575,00 | — | Pré-ordem de bloqueio |
| [T0] | R$ 5.491,00 | -98,8% | Após intimação |

> **Enquadramento:** possível fraude à execução (art. 792 CPC) e ocultação patrimonial (art. 50 CC).

### Saída
- Relatório de saúde do sistema (técnico)
- Mapa de inconsistências jurídicas identificadas
- Alimenta o módulo 3 (Dependency Update Check)
