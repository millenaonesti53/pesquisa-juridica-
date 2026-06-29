---
name: premortem-tese-financeira
description: Aplica o metodo adversarial de pre-mortem a teses financeiras, contabeis e de avaliacao patrimonial. Submete a tese (valuation, apuracao de haveres, money trail, fraude a execucao, parecer contabil) ao steelman do avaliador adverso, audita TODA objecao de premissa, metodo e dado, mapeia vulnerabilidades em cenarios melhor/provavel/risco com sensibilidade, e desemboca em parecer Diagnostico-Evidencia-Implicacoes-Cenarios-Estrategia-Acao com premissas e limites explicitados. Use SEMPRE que o usuario for construir, defender, revisar ou "blindar" tese financeira ou contabil contestada por perito adverso, auditor ou banca — valuation, apuracao de haveres, desconto de iliquidez, distribuicao disfarcada, rastreio patrimonial. Dispara com "qual a fragilidade desse valuation", "como o perito adverso vai atacar", "blinda esse calculo", "que premissa nao se sustenta", "onde o numero quebra". Chama o nucleo metodo-adversarial-nucleo. Output e instrumento interno; versao pericial exige profissional habilitado (CRC).
---

# Pré-mortem de Tese Financeira

Esta skill aplica o método adversarial (núcleo em `metodo-adversarial-nucleo`) ao domínio financeiro-contábil. Leia o núcleo e seu `references/movimentos.md` para a mecânica dos 6 movimentos; esta skill fornece o vocabulário de premissa/método/evidência e o formato de parecer.

## Premissa

Um número financeiro contestado não vale pela sua precisão aparente, mas pela robustez das premissas que o sustentam. O avaliador da parte contrária não vai atacar o resultado — vai atacar a **premissa** que o gera, o **método** que o calcula, e o **dado** que o alimenta. Uma tese financeira que só apresenta o resultado favorável, sem blindar premissa/método/dado, cai no primeiro parecer divergente. O método inverte: **toda objeção técnica previsível é antecipada e neutralizada, e todo limite do método é declarado antes que o adversário o explore.**

Declarar o próprio limite não enfraquece — fortalece: o parecer que reconhece a faixa de incerteza é mais crível do que o que finge precisão cirúrgica. **Output é instrumento interno; versão pericial exige assinatura de profissional habilitado (CRC).**

## Ciclo aplicado ao financeiro

### FASE 1 — Reconstrução da tese própria
Fixe a tese e ancore cada elo:
- **Tese central** em proposição verificável: não "o ativo vale muito", mas "o equity do FIP na data-base X equivale a R$ N, sob o método M, premissas P1..Pn, com base nos documentos D1..Dn".
- **Cadeia DADO → MÉTODO → RESULTADO**: cada input (demonstração, ato societário, extrato), o tratamento aplicado, o output.
- **Fato vs. premissa vs. estimativa**: separe o que é dado auditado, o que é premissa adotada, e o que é estimativa. Marque premissas e estimativas explicitamente — é onde o avaliador adverso entra.

### FASE 2 — Steelman do avaliador adverso `[STEELMAN]`
Construa o melhor parecer divergente possível — mais forte do que o perito da outra parte provavelmente fará. Ataque nos **três planos**:
- **Premissa**: qual premissa adotada o adversário substituiria, e por qual (taxa de desconto, going concern vs. liquidação, data-base, desconto de iliquidez/restrição de transferência, taxa de crescimento).
- **Método**: qual metodologia alternativa o adversário aplicaria (fluxo de caixa descontado vs. múltiplos vs. valor patrimonial vs. cláusula contratual de saída) e por que mudaria o resultado.
- **Dado**: qual input o adversário questionaria (qualidade da demonstração, ausência de documento de origem, intercompany não eliminado, ativo/passivo não reconhecido).

Regra: se você não consegue produzir um parecer divergente que um avaliador competente assinaria, não conhece a própria fragilidade.

### FASE 3 — Auditoria de objeção técnica `[AUDITORIA]`
Tabela de três colunas:

| Objeção técnica | Força / por quê | Neutralização |
|---|---|---|
| (o que o perito adverso dirá) | alta/média/baixa + razão | dado de suporte, sensibilidade, premissa alternativa testada, ou limite declarado |

Regras de domínio:
- Objeção **sem boa resposta** vira: (a) análise de sensibilidade (mostrar o resultado sob a premissa adversa), (b) faixa de valor em vez de ponto único, ou (c) limite declarado e risco assumido.
- Para toda premissa-chave, rode **sensibilidade**: como o resultado muda se a premissa for substituída pela do adversário. Premissa cujo resultado vira de sinal sob perturbação razoável é o ponto frágil — exponha-a você, com a faixa.
- Distinga objeção de **premissa** (escolha de input), de **método** (técnica de cálculo) e de **dado** (qualidade do insumo) — neutralizam-se de formas diferentes.

### FASE 4 — Mapa de vulnerabilidade e cenários
Matriz melhor / provável / risco, com probabilidade:
- **Vetor de ataque mais provável** do avaliador adverso (qual premissa/método/dado ele mira primeiro).
- **Melhor cenário**: valor sustentado integralmente — condições.
- **Cenário provável**: faixa de valor que realisticamente prevalece após o confronto pericial; ponto de maior divergência.
- **Cenário de risco**: como o valor desaba (qual premissa cai e quanto custa).
- **Timing**: que documento de origem produzir primeiro (certificados de subscrição, registro de cotistas, deeds de integralização), qual prova pericial requerer, sequência de quesitos.

### FASE 5 — Tradução em parecer
Estruture Diagnóstico → Evidência → Implicações → Cenários → Estratégia → Ação:
1. **Diagnóstico**: a tese de valor/caracterização, em registro técnico sóbrio `[SOBRIO]`.
2. **Evidência**: dado por dado, com fonte; método explicitado; premissas listadas.
3. **Implicações**: o que o número significa para a partilha/execução/caracterização.
4. **Cenários**: a matriz da Fase 4, com sensibilidade.
5. **Estratégia / Ação**: o que produzir, requerer, quesitar — e em que ordem.
- **Limites do método declarados** em seção própria (o que o parecer não afirma, qual a faixa de incerteza).
- Marque técnicas entre colchetes na versão de trabalho; gere versão limpa.
- Antes de entregar qualquer planilha de suporte, rode a validação (`recalc.py`, no padrão do usuário). Campos-resumo oficiais de cada documento são as totalizações autoritativas; somas linha a linha são indicativas.
- Carimbo: **"INSTRUMENTO INTERNO DE TRABALHO — NÃO PROTOCOLAR. Versão pericial exige subscrição de profissional habilitado (CRC)."**

### FASE 6 — Teste de convicção `[CONVICCAO]`
Ofereça submeter ao agente `advogado-do-diabo` (que opera também como perito-contador adverso), atacando premissa/método/dado com as melhores objeções reais. A tese passa quando o valor resiste ou quando a faixa é honestamente ajustada. Escreva: "mesmo sob a premissa adversa X, a conclusão subsiste porque Y / a faixa se desloca para Z mas a tese central permanece".

## Calibração

- **Valuation/laudo colado + "onde o número quebra"** → Fases 2-4 direto.
- **Construção do zero** → Fase 1.
- **Só o pré-mortem técnico** → Fases 2-4, sem redigir parecer.
- **Estressar a tese pronta** → Fase 6 (agente).
- **Só formular quesitos contábeis** → `[CALIBRADA]` para quesitos que forcem reconstrução documental sem admitir evasiva ("não é possível aferir" sem justificar a ausência do documento).

## Guardrails de domínio

1. **Premissa explícita.** Toda premissa e estimativa é declarada e justificada. Premissa oculta é o vetor de ataque nº 1.
2. **Sensibilidade obrigatória** para premissa-chave. Faixa de valor, não falsa precisão de ponto único.
3. **Limites do método declarados.** O parecer afirma o que pode sustentar e reconhece o que não pode.
4. **Caracterização "em tese"** quando a tese financeira tocar conduta (distribuição disfarçada, fraude a execução, esvaziamento): registro hipotético, sem afirmação categórica.
5. **Validação antes da entrega**: `recalc.py` em toda planilha; campos-resumo oficiais como totalizações autoritativas; Python com encoding explícito (nunca Perl em UTF-8).
6. **Assinatura de profissional habilitado (CRC)** para versão pericial. A skill produz instrumento interno.
7. **Steelman honesto** do avaliador adverso — o melhor parecer divergente, não um fraco. E não se manipula perito ou julgador: o método antecipa e robustece, não induz.
