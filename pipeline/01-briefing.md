# 🌅 Módulo 1 — Briefing

**Pipeline Cognitivo Corporativo (PhD TI) | Estágio 1/5**

---

## Função Tecnológica

Agregar dados de múltiplas fontes e gerar o **daily intelligence report** consolidado:

- Google Calendar — compromissos, audiências, prazos
- Gmail — respostas bancárias, ofícios, decisões judiciais
- Slack — comunicações internas do Núcleo de Governança
- CVM — atualizações de FIPs e fundos monitorados
- SISBAJUD — ordens de bloqueio, respostas e códigos

## Função Jurídica

Atualizar o CLO (Chief Legal Officer) e o Núcleo de Governança sobre:

1. Novos bloqueios determinados
2. Respostas bancárias recebidas e seus códigos SISBAJUD
3. Movimentações suspeitas identificadas no período
4. Atualizações de FIPs (Fundos de Investimento em Participações)

## Rotina Integrada

### Entrada
- Whole Money Trail do dia anterior (atualizado)
- Status das respostas bancárias pendentes

### Processamento

```
Passo 1 — Carregar Whole Money Trail do dia anterior
Passo 2 — Atualizar status das instituições:
  - Código 98: não respondeu → escalar alerta
  - Código 13: respondeu sem saldo → cruzar com IRPF e extratos
Passo 3 — Para cada instituição monitorada:
  a. Verificar código SISBAJUD mais recente
  b. Comparar saldo atual × histórico
  c. Classificar risco (normal / atenção / crítico)
  d. Gerar alerta se:
     - Código 98 (não respondeu)
     - Código 13 com histórico de saldo positivo
     - Variação > 50% sem justificativa registrada
Passo 4 — Gerar alertas automáticos por instituição
```

### Alertas Automáticos — Gatilhos Ativos

| Instituição | Gatilho | Prioridade |
|-------------|---------|------------|
| FRAM | Não resposta (cód. 98) | CRÍTICA |
| OSLO | Não resposta (cód. 98) | CRÍTICA |
| BTG | Esvaziamento tático (saldo zero repetido) | ALTA |
| Itaú | Esvaziamento tático (R$ 469.575 → R$ 5.491) | ALTA |

### Saída
- Relatório de inteligência diária (formato: `notas/briefing-AAAA-MM-DD.md`)
- Lista de pendências para o Health Check

---

## Template de Saída

```markdown
# Briefing Diário — [DATA]

## Resumo Executivo
[2-3 frases sobre o estado geral da investigação]

## Novos Eventos
- [ ] [Evento 1]
- [ ] [Evento 2]

## Status SISBAJUD
| Instituição | Código | Saldo Reportado | Variação | Risco |
|-------------|--------|-----------------|----------|-------|

## Alertas Ativos
[Lista de alertas críticos]

## Próximos Passos
[Ações para o dia]
```
