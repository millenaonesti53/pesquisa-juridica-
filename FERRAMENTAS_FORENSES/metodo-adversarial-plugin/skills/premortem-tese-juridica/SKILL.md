---
name: premortem-tese-juridica
description: Aplica o metodo adversarial de pre-mortem a teses, pecas e pareceres juridicos. Submete a tese ao steelman do adversario, audita TODA impugnacao antecipavel (de fato, prova e direito) antes que a parte contraria a faca, mapeia vulnerabilidades em cenarios melhor/provavel/risco, e desemboca em peca FATO para PROVA para NORMA para PEDIDO com cada objecao forte ja neutralizada no corpo. Use SEMPRE que o usuario for construir, defender, revisar ou "blindar" tese juridica, peticao, contestacao, agravo, memorial, parecer ou quesito que sera lido por juiz, perito ou parte adversa — em litigio, familia, partilha, execucao ou materia forense-patrimonial. Dispara com "blinda essa tese", "como o reu/autor vai impugnar", "qual o ponto fraco dessa peca", "antecipa a contestacao", "testa esse argumento juridico", "onde o juiz vai resistir", "pre-mortem dessa peticao". Chama o nucleo metodo-adversarial-nucleo. Output e instrumento interno; protocolo exige subscricao de advogado(a) inscrito(a) na OAB.
---

# Pré-mortem de Tese Jurídica

Esta skill aplica o método adversarial (núcleo em `metodo-adversarial-nucleo`) ao domínio jurídico-processual. Leia o núcleo e seu `references/movimentos.md` para a mecânica dos 6 movimentos; esta skill fornece o vocabulário forense e o formato de peça.

## Premissa

A peça jurídica é o único produto cujo destinatário inclui alguém pago para derrubá-la. Construir só a fundamentação positiva da própria tese é entregar ao adversário a primeira manifestação como demolição. O método inverte: **toda impugnação previsível é verbalizada e neutralizada dentro da própria peça, antes de ser feita.** Isso não é defensividade — é controle de enquadramento.

Esta abordagem foi endurecida por experiência adversarial real: peças sem subscrição de advogado(a) já foram usadas como vetor de impugnação. Por isso, **todo output desta skill é instrumento interno de trabalho e exige assinatura de advogado(a) inscrito(a) na OAB para protocolo.**

## Ciclo aplicado ao jurídico

### FASE 1 — Reconstrução da tese própria
Fixe a tese em proposição falsificável e ancore cada elo:
- **Tese central**: não "o réu agiu mal", mas "o réu praticou a conduta X (fato), vedada pela norma Y (direito), comprovada por Z (prova)".
- **Cadeia FATO → PROVA → NORMA**: para cada fato afirmado, a prova que o sustenta (fls., documento, perícia) e a norma que o qualifica.
- **Provado vs. assumido**: marque com `[A CONFIRMAR]` ou citação de fólio. O que está assumido sem prova é o vetor de entrada do adversário.

### FASE 2 — Steelman do adversário `[STEELMAN]`
Construa a melhor contestação possível — mais forte do que a parte contrária provavelmente fará:
- A tese oposta na versão mais defensável.
- As melhores objeções em **três planos**: de **fato** (a narrativa alternativa dos mesmos fatos), de **prova** (o que falta, o que é indiciário, o que é impugnável), de **direito** (a norma/precedente/distinção que o adversário invocará).
- Inclua preliminares que a parte contrária pode suscitar (incompetência, litispendência, ilegitimidade, prescrição/decadência) e avalie a força real de cada uma — sem subestimar nem inflar.

### FASE 3 — Auditoria de impugnação `[AUDITORIA]`
Tabela de três colunas para toda objeção antecipável:

| Impugnação | Força / por quê | Neutralização no corpo |
|---|---|---|
| (o que o adversário dirá) | alta/média/baixa + razão | citação, prova, distinção, contraprova, ou reconhecimento honesto do limite |

Regras de domínio:
- Objeção **sem boa resposta** vira: (a) requerimento de prova (exibição art. 396 CPC, perícia, testemunha), (b) reformulação para pedido mais defensável, ou (c) risco assumido conscientemente e registrado.
- Distinga impugnação **processual** (preliminar) de **material** (mérito) — neutralizam-se em seções diferentes da peça.
- Para cada precedente que o adversário invocará, prepare o **distinguishing** (por que o caso é diferente) ou a **superação** (por que o precedente não prevalece).

### FASE 4 — Mapa de vulnerabilidade e cenários
Matriz no padrão melhor / provável / risco, com probabilidade estimada:
- **Vetor de ataque mais provável** da parte contrária.
- **Melhor cenário**: tese acolhida — condições e o que a sustenta.
- **Cenário provável**: o que realisticamente o juízo faz, onde a peça é contestada, qual o ponto de maior atrito.
- **Cenário de risco**: como a tese cai (improcedência, extinção, preliminar acolhida) e qual o gatilho.
- **Timing processual**: o que protocolar antes do quê, qual prova produzir primeiro, qual incidente precede qual, janelas recursais.

### FASE 5 — Tradução em peça
Estruture FATO → PROVA → NORMA → PEDIDO, com a auditoria já incorporada:
1. **Fatos**: narrativa em registro sóbrio `[SOBRIO]`, "em tese" (CF art. 5º, LVII), cada fato com fólio.
2. **Direito**: fundamentação positiva + objeções antecipadas neutralizadas `[NOMEACAO]` ("poder-se-ia objetar que… contudo…").
3. **Pedido**: específico, líquido quando possível, com pedidos subsidiários para os cenários de risco mapeados.
- Marque técnicas entre colchetes na versão de trabalho; gere versão limpa para protocolo.
- Carimbo obrigatório: **"INSTRUMENTO INTERNO DE TRABALHO — NÃO PROTOCOLAR. Versão para protocolo exige subscrição de advogado(a) inscrito(a) na OAB."**

### FASE 6 — Teste de convicção `[CONVICCAO]`
Ofereça submeter ao agente `advogado-do-diabo`, que assume o papel da parte contrária e impugna a peça com as melhores objeções reais. A tese passa quando resiste — ou quando as falhas reveladas são corrigidas. Escreva o parágrafo "mesmo que se conceda X, a tese subsiste porque Y"; se não for possível escrevê-lo honestamente, reformule.

## Calibração

- **Peça/tese colada + "onde isso quebra"** → Fases 2-4 direto.
- **Construção do zero** → Fase 1.
- **Só o pré-mortem estratégico** → Fases 2-4, sem redigir peça.
- **Estressar a tese pronta** → Fase 6 (agente).
- **Só quesitos** → aplique `[CALIBRADA]` (ver movimentos.md) para formular quesitos que não entreguem resposta ao perito adversário.

## Guardrails de domínio

1. **Registro "em tese"** para toda caracterização de conduta (CF art. 5º, LVII). Nunca afirmação categórica de crime/fraude sem trânsito.
2. **Toda asserção factual com fólio (fls.) ou marcador `[A CONFIRMAR]`.** Suposição não vira fato.
3. **Política cumulativo-expansiva**: ao revisar peça existente, nunca delete conteúdo validado; só adicione com racional registrado.
4. **Subscrição de advogado(a)** obrigatória para protocolo. A skill produz instrumento interno; a versão protocolável é responsabilidade do(a) advogado(a) inscrito(a).
5. **Não se manipula o juízo.** O método antecipa objeção e robustece fundamento — não induz, pressiona ou fabrica concessão de quem julga.
6. **Steelman honesto.** A contestação reconstruída é a mais forte possível, não um espantalho. Steelman fraco produz peça falsamente segura.
