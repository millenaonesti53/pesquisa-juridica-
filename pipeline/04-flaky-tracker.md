# Módulo 4 — 🧪 Flaky Test Tracker

**Pipeline Cognitivo Corporativo | Estágio 4/5 | v2.0**

---

## Visão Geral

Aplica metodologia de testes de consistência (inspirada em software quality assurance) à investigação patrimonial: identifica respostas e declarações que se comportam de forma "flaky" — inconsistente, imprevisível ou contraditória — revelando padrões de ocultação.

---

## Função Tecnológica

Identificar inconsistências estatísticas e padrões anômalos:

- PLs variando sem justificativa econômica documentada
- Respostas bancárias incoerentes entre si ou com o histórico
- Divergências entre fontes primárias independentes
- Padrões temporais suspeitos (ex.: esvaziamento correlacionado com datas de intimação)

---

## Função Jurídica

Testar a consistência das alegações do devedor e das instituições financeiras:

| Teste | Pergunta central | Resultado esperado se houver ocultação |
|-------|-----------------|----------------------------------------|
| Iliquidez | A alegação de iliquidez dos FIPs é sustentável? | PL positivo contradiz a alegação |
| Esvaziamento | Há padrão temporal de redução de saldo antes de ordens? | Correlação com datas de intimação |
| Ocultação sistêmica | Múltiplas instituições apresentam o mesmo padrão? | Coordenação entre entidades |

---

## Rotina Integrada

### Casos Marcados como "Flaky"

#### BTG — Saldo Zero Repetido com Movimentação Prévia

```
Padrão detectado:
  Saldo reportado (SISBAJUD):  R$ 0,00 (repetido em múltiplas consultas)
  CDB registrado (CVM/IRPF):  R$ 650.758,60
  Histórico:                   Movimentação positiva em períodos anteriores

Análise estatística:
  Probabilidade de saldo zero natural: baixa
  Correlação com datas de intimação:  verificar
  Classificação:                       FLAKY — resposta inconsistente

Enquadramento jurídico:
  Art. 774 CPC — declaração falsa ao SISBAJUD é ato atentatório
  Art. 835, IX CPC — CDB é bem penhorável

Ações:
  → Peticionar novo bloqueio com prazo reduzido de resposta
  → Requerer extrato dos últimos 24 meses do CDB
  → Representar ao BCB caso o extrato contradiga a resposta SISBAJUD
```

#### Itaú — Esvaziamento Tático

```
Padrão detectado:
  Saldo pré-intimação: R$ 469.575,00
  Saldo pós-intimação: R$ 5.491,00
  Variação:            -98,8% em período correlacionado com a intimação

Análise estatística:
  Variação incompatível com operação normal de conta corrente
  Timing correlacionado com recebimento da ordem judicial
  Classificação: FLAKY — esvaziamento tático provável

Enquadramento jurídico:
  Art. 792 CPC — fraude à execução
  Art. 171 CP — estelionato (se verificado dolo)

Ações:
  → Requerer extratos detalhados do período T-30 a T+30
  → Identificar destinatários de todas as transferências no período
  → Peticionar bloqueio nas contas de destino identificadas
  → Instruir o juízo sobre o timing suspeito
```

#### FRAM / OSLO — Ausência de Resposta Sistemática e Coordenada

```
Padrão detectado:
  FRAM: cód. 98 em múltiplas ordens SISBAJUD (ativo: R$ 3.877.255,47)
  OSLO: cód. 98 em múltiplas ordens SISBAJUD (ativo: a apurar)
  Padrão: ambas as instituições; mesmo comportamento; ausência coordenada

Análise estatística:
  Coincidência de não resposta em múltiplas ocasiões: estatisticamente improvável
  Possível coordenação entre FRAM e OSLO: investigar vínculos societários
  Classificação: FLAKY — não resposta sistemática e possivelmente coordenada

Enquadramento jurídico:
  Art. 774 CPC — ato atentatório à dignidade da justiça
  Lei 4.595/64 — competência do BCB (descumprimento de normas)
  CVM — poder disciplinar sobre gestoras de FIPs

Ações:
  → Peticionar multa por descumprimento de ordem judicial (art. 774 CPC)
  → Requerer intimação pessoal dos administradores de FRAM e OSLO
  → Investigar vínculos societários entre FRAM e OSLO (CVM, Receita)
  → Representar ao BCB e à CVM com documentação do padrão
```

---

## Matriz de Inconsistência Consolidada

| Instituição | Tipo de Flakiness | Frequência | Impacto Financeiro | Ação Prioritária |
|-------------|-------------------|------------|-------------------|-----------------|
| BTG | Saldo zero repetido | Alta | R$ 650.758,60 | Novo bloqueio + extrato 24 meses |
| Itaú | Esvaziamento tático | Pontual / cirúrgico | R$ 464.084,00 | Rastrear transferências + bloquear destino |
| FRAM | Não resposta (98) | Sistemática | R$ 3.877.255,47 | Multa + BCB + CVM |
| OSLO | Não resposta (98) | Sistemática | A apurar | Multa + investigar vínculos com FRAM |

---

## Teste de Iliquidez dos FIPs

```
Tese do devedor: FIPs são ilíquidos e impenhoráveis.

Contra-teste:
  1. Verificar se há resgate de cotas após o início do litígio
     → Se sim: o FIP é líquido o suficiente para resgates
  2. Verificar se há distribuição de rendimentos
     → Se sim: gera fluxo penhorável independente da iliquidez do principal
  3. Verificar se o PL real justifica a alegação de iliquidez total
     → FRAM XIV: PL R$ 3.877.255,47 — iliquidez total não demonstrada
  4. Verificar se há mercado secundário para as cotas
     → A apurar

Resultado atual:
  FRAM XIV:         PL R$ 3.877.255,47 — iliquidez não demonstrada → contestar
  Bonifácio FIP:    criado pós-litígio → Classe J ineficaz (art. 792 CPC)
  Ajaccio:          inconsistência temporal → apurar antes de concluir
```

---

## Saída do Módulo

- **Relatório de inconsistências** classificadas por risco e impacto financeiro
- Lista de ações jurídicas prioritárias ranqueadas por urgência
- **Evidências formatadas** para o Módulo 5 (PR Review Digest)

---

## Legislação de Referência

- Art. 171, CP — Estelionato
- Art. 50, CC — Desconsideração da personalidade jurídica
- Art. 774, CPC — Atos atentatórios à dignidade da justiça
- Art. 792, CPC — Fraude à execução
- Art. 835, IX, CPC — Penhorabilidade de cotas de fundos
- Lei 4.595/64 — Supervisão do BCB sobre instituições financeiras
- Lei 9.613/98 — Lavagem de capitais
