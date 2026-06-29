# Taxonomia de objeção técnica e exemplo aplicado — financeiro

Apoio à skill premortem-tese-financeira. Catálogo de vetores de objeção para a auditoria (Fase 3) e um exemplo de valuation ponta a ponta com sensibilidade.

## Catálogo de objeções técnicas

Checklist da Fase 3 — para cada vetor, "o avaliador adverso tem munição aqui?".

### Plano da premissa
- **Data-base**: a premissa adota a data correta? Avaliar na data da separação de fato vs. na data da partilha muda o valor.
- **Going concern vs. liquidação**: o ativo é avaliado em continuidade ou em cenário de desinvestimento? Muda a base.
- **Taxa de desconto / custo de capital**: a taxa adotada é defensável? O adversário a sobe (reduz valor) ou desce (aumenta).
- **Desconto por iliquidez / restrição de transferência**: cláusula de saída forçada (ex.: acordo de cotistas) impõe desconto? Qual percentual é defensável?
- **Taxa de crescimento / perpetuidade**: premissa de crescimento sustentável vs. otimista.
- **Prêmio/desconto de controle**: a participação dá controle? Minoritária sofre desconto.

### Plano do método
- **DCF vs. múltiplos vs. valor patrimonial vs. cláusula contratual**: qual o método primário e por quê? O adversário aplica o que favorece a posição dele.
- **Cláusula contratual de saída como piso/teto**: há fórmula no acordo (ex.: valor/cota + índice + juros)? Ela prevalece sobre o método de mercado?
- **Distinção valor de negociação vs. valor justo**: número de LOI/term sheet é valor prospectivo de negociação, não valor justo na data-base — não confundir.
- **Consistência metodológica**: o mesmo método foi aplicado a ativos comparáveis?

### Plano do dado
- **Qualidade da demonstração**: auditada? Republicada? Com ressalva?
- **Documento de origem ausente**: certificado de subscrição, registro de cotistas, deed de integralização — sem origem, a composição é afirmada, não comprovada. Ônus de quem alega composição favorável.
- **Intercompany não eliminado**: fluxos entre entidades do grupo inflam/deflam.
- **Ativo/passivo não reconhecido**: passivo oculto, ativo não contabilizado, contingência não provisionada.
- **Distribuição disfarçada de lucro**: retiradas travestidas; teste de pró-labore vs. distribuição.

## Exemplo aplicado ponta a ponta (sintético)

**Tese:** o equity do FIP na data-base equivale a no mínimo R$ 108M (ancorada em LOI ago/2025).

### Fase 1 — Tese fixada
"O equity equivale a ≥ R$108M na data-base, conforme valor confessado em LOI de ago/2025 (D1)."
Premissa adotada: o valor de LOI reflete valor justo na data-base. **Estimativa** (não dado auditado): composição da carteira na data-base.

### Fase 2 — Steelman do avaliador adverso `[STEELMAN]`
"O valor de R$108M é valor de negociação prospectivo, sob premissas de going concern e liquidez futura. Aplicá-lo como piso na data-base (a) confunde valor de negociação com valor justo, (b) ignora o desconto por iliquidez e por restrição de transferência imposto pela cláusula 9.7.1 do acordo de cotistas, e (c) desconsidera que a própria cláusula de saída estabelece fórmula distinta (valor/cota + índice + juros) que prevalece sobre o número de mercado. O valor defensável seria o da fórmula contratual, materialmente inferior."

### Fase 3 — Auditoria `[AUDITORIA]`
| Objeção | Força | Neutralização |
|---|---|---|
| LOI = valor de negociação, não valor justo | Alta | Sustentar que a LOI é confissão de valor mínimo reconhecido pelas próprias partes; usar como piso indiciário, não como laudo; reforçar com método independente |
| Cláusula 9.7.1 impõe desconto de iliquidez | Alta | Rodar sensibilidade: valor sob desconto de 20%/30%/40%; mostrar faixa. Distinguir gatilho de saída (constrição judicial) que pode afastar o desconto voluntário |
| Fórmula contratual prevalece | Média | Distinguir cláusula de saída por divórcio (7.3.5, metodologia de avaliação) da de constrição (9.7.1, piso) — a aplicável depende do fato gerador |
| Composição da carteira não comprovada | Alta | Requerer exibição dos documentos de origem; ônus de provar composição favorável é de quem a alega |

### Fase 4 — Cenários (com sensibilidade)
- **Melhor:** R$108M sustentado como piso (juízo acolhe LOI como confissão). Probabilidade estimada: baixa-média.
- **Provável:** faixa R$65M–95M após aplicação de desconto de iliquidez parcial e confronto pericial. Ponto de divergência: percentual do desconto e método primário.
- **Risco:** valor reduzido à fórmula contratual (9.7.1), materialmente inferior. Gatilho: juízo aceita prevalência da cláusula de saída + ausência de documento de composição.
- **Sensibilidade do desconto de iliquidez:**

| Desconto aplicado | Valor resultante (sobre R$108M) |
|---|---|
| 0% | R$108M |
| 20% | R$86,4M |
| 30% | R$75,6M |
| 40% | R$64,8M |

- **Timing:** requerer exibição dos documentos de origem (certificados de subscrição, registro de cotistas) ANTES do confronto pericial — a composição documental sustenta a faixa superior em todos os cenários.

### Fase 5 — Esqueleto do parecer
Diagnóstico (tese de valor) → Evidência (LOI + método independente + premissas) → Implicações (impacto na meação) → Cenários (matriz + sensibilidade) → Estratégia/Ação (exibição → perícia → quesitos). Limites declarados (faixa de incerteza, dependência do documento de origem). `recalc.py` antes da planilha. Carimbo de instrumento interno (CRC para versão pericial).

### Fase 6 — Convicção `[CONVICCAO]`
"Mesmo sob a premissa adversa de desconto de iliquidez de 30%, a conclusão central subsiste: o valor (R$75,6M) permanece materialmente superior ao da fórmula contratual isolada, e a confissão de R$108M na LOI fixa o piso indiciário do reconhecimento das próprias partes. A faixa se desloca, a tese de subavaliação deliberada permanece."
