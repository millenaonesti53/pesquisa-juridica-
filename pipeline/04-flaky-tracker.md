# 🧪 Módulo 4 — Flaky Test Tracker

**Pipeline Cognitivo Corporativo (PhD TI) | Estágio 4/5**

---

## Função Tecnológica

Identificar inconsistências estatísticas e padrões anômalos nos dados:

- PLs variando sem justificativa econômica documentada
- Respostas bancárias incoerentes entre si ou com o histórico
- Divergências entre fontes primárias independentes
- Padrões temporais suspeitos (ex.: esvaziamento pré-ordem judicial)

## Função Jurídica

Testar a consistência das alegações do devedor e identificar padrões de ocultação:

1. **Teste de iliquidez** — a alegação de iliquidez dos FIPs é sustentável?
2. **Teste de esvaziamento** — há padrão temporal de redução de saldo antes de ordens?
3. **Teste de ocultação sistêmica** — múltiplas instituições apresentam o mesmo padrão?

## Rotina Integrada

### Resumo — Marcações Flaky Ativas

| Instituição | Classificação | Evidência Principal |
|-------------|---------------|---------------------|
| BTG | FLAKY — saldo zero repetido | CDB R$ 650.758,60 com movimentação prévia |
| Itaú | FLAKY — esvaziamento tático | -98,8% correlacionado com intimação judicial |
| FRAM | FLAKY — não resposta sistemática | Código 98 repetido em múltiplas ordens |
| OSLO | FLAKY — não resposta sistemática | Código 98 repetido; possível coordenação com FRAM |

### Casos Marcados como "Flaky" (Inconsistentes)

#### BTG — Saldo Zero Repetido com Movimentação Prévia

```
Padrão detectado:
  - Saldo reportado: R$ 0,00 (repetido em múltiplas consultas)
  - Histórico de movimentação: positivo em períodos anteriores
  - CDB registrado: R$ 650.758,60

Análise estatística:
  - Probabilidade de saldo zero natural: baixa
  - Correlação com datas de intimação: verificar
  - Classificação: FLAKY — resposta inconsistente

Ação jurídica:
  - Peticionar novo bloqueio com prazo reduzido
  - Requerer extrato dos últimos 12 meses
  - Enquadrar em possível desobediência à ordem judicial
```

#### Itaú — Esvaziamento Tático

```
Padrão detectado:
  - Saldo pré-intimação: R$ 469.575,00
  - Saldo pós-intimação: R$ 5.491,00
  - Variação: -98,8% em período suspeito

Análise estatística:
  - Variação incompatível com operação normal de conta
  - Timing correlacionado com intimação judicial
  - Classificação: FLAKY — esvaziamento tático provável

Ação jurídica:
  - Requerer extratos detalhados do período
  - Identificar destinatários das transferências
  - Peticionar bloqueio das contas de destino
  - Enquadrar: art. 792 CPC + art. 171 CP
```

#### FRAM / OSLO — Ausência de Resposta Sistemática

```
Padrão detectado:
  - FRAM: código 98 em múltiplas ordens SISBAJUD
  - OSLO: código 98 em múltiplas ordens SISBAJUD
  - Ausência coordenada de resposta

Análise estatística:
  - Ambas as instituições: mesmo padrão de não resposta
  - Possível coordenação entre as entidades
  - Classificação: FLAKY — não resposta sistemática

Ação jurídica:
  - Peticionar multa por descumprimento de ordem judicial
  - Requerer intimação pessoal dos administradores
  - Investigar vínculos entre FRAM e OSLO
  - Representar ao BCB e à CVM por desobediência
```

### Matriz de Inconsistência

| Instituição | Tipo de Flakiness | Frequência | Impacto | Ação Prioritária |
|-------------|-------------------|------------|---------|-----------------|
| BTG | Saldo zero repetido | Alta | R$ 650.758,60 | Novo bloqueio + extrato |
| Itaú | Esvaziamento tático | Pontual | R$ 464.084,00 | Rastrear transferências |
| FRAM | Não resposta (98) | Sistemática | R$ 3.877.255,47 | Multa + BCB/CVM |
| OSLO | Não resposta (98) | Sistemática | A apurar | Multa + investigar vínculos |

### Teste de Iliquidez dos FIPs

```
Premissa alegada: FIPs são ilíquidos e impenhoráveis
Teste:
  1. Verificar se há resgate de cotas após o início do litígio → se sim, líquido
  2. Verificar se há distribuição de rendimentos → se sim, gera fluxo penhorável
  3. Verificar se o PL real justifica a iliquidez alegada
  4. Verificar se há mercado secundário para as cotas

Resultado atual:
  - FRAM XIV: PL de R$ 3.877.255,47 — iliquidez não demonstrada
  - Classe J (Bonifácio): criação pós-litígio — invalida impenhorabilidade
```

### Saída
- Relatório de inconsistências classificadas por risco
- Lista de ações jurídicas prioritárias
- Evidências para o PR Review Digest
