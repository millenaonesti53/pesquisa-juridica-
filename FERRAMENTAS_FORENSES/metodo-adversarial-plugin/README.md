# metodo-adversarial

Método de análise adversarial por **pré-mortem de tese**, para trabalho jurídico-forense e financeiro-contábil de alto risco.

O plugin adapta a *arquitetura cognitiva* da negociação tática de alto risco (método Chris Voss / Black Swan Group) — diagnosticar antes de produzir, verbalizar a objeção do outro antes que ele a faça, calibrar perguntas, manter registro sóbrio — e a reconstrói sobre fundamentação técnica legítima. **Não** transpõe a camada de manipulação (não se induz juiz nem perito); transpõe o **rigor antecipatório**.

## A premissa

Uma tese não está pronta quando você a acha convincente. Está pronta quando **sobrevive ao melhor ataque que o adversário poderia montar** — e quando esse ataque já foi neutralizado dentro do próprio corpo da peça ou do parecer. O analista que só reúne argumentos a favor da própria posição constrói um castelo para o adversário demolir na primeira manifestação.

## A tradução do método

| Camada de negociação | Tradução forense legítima | Marcador |
|---|---|---|
| Tactical empathy | **Steelman do adversário** — reconstruir o melhor argumento contrário, não um espantalho | `[STEELMAN]` |
| Accusation audit | **Auditoria de impugnação** — antecipar e neutralizar toda objeção antes dela | `[AUDITORIA]` |
| Labeling | **Nomeação da objeção** — verbalizar a leitura cética do julgador e desarmá-la | `[NOMEACAO]` |
| Calibrated questions | **Pergunta/quesito calibrado** — que não entrega resposta ao adversário | `[CALIBRADA]` |
| That's right trigger | **Teste de convicção** — a tese só passa quando resiste ao próprio steelman | `[CONVICCAO]` |
| Late-night FM DJ voice | **Registro sóbrio** — "em tese", sem hipérbole; precisão persuade | `[SOBRIO]` |

## O ciclo

1. **Reconstrução da tese própria** — proposição falsificável; separa o provado do assumido.
2. **Steelman do adversário** — o melhor caso contrário possível.
3. **Auditoria de impugnação/objeção** — tabela impugnação / força / neutralização.
4. **Mapa de vulnerabilidade** — cenários melhor / provável / risco, com probabilidade e timing.
5. **Tradução em produto** — peça (FATO→PROVA→NORMA→PEDIDO) ou parecer (Diagnóstico→Evidência→Implicações→Cenários→Estratégia→Ação).
6. **Teste de convicção** — submeter ao agente que ataca com as melhores objeções reais.

## Componentes

| Tipo | Nome | Função |
|---|---|---|
| Skill | `metodo-adversarial-nucleo` | Motor metodológico abstrato; usável para tese de qualquer natureza. |
| Skill | `premortem-tese-juridica` | Aplicação ao domínio jurídico (prova / norma / impugnação); produto: peça. |
| Skill | `premortem-tese-financeira` | Aplicação ao domínio financeiro (premissa / método / dado); produto: parecer com sensibilidade. |
| Comando | `/metodo-adversarial:premortem-juridico` | Atalho do pré-mortem jurídico. |
| Comando | `/metodo-adversarial:premortem-financeiro` | Atalho do pré-mortem financeiro. |
| Agente | `advogado-do-diabo` | Encarna a parte contrária / perito adverso e estressa a tese até ela resistir ou ser corrigida. |

## Instalação

### Via marketplace (local)
```bash
/plugin marketplace add ./metodo-adversarial-plugin
/plugin install metodo-adversarial@metodo-adversarial-marketplace
```

### Via diretório de skills
Coloque a pasta `metodo-adversarial-plugin/` num diretório de plugins do Claude Code; é descoberta na próxima sessão como `metodo-adversarial@skills-dir`.

## Primeiro uso

```
/metodo-adversarial:premortem-juridico Tese: o bloqueio SISBAJUD sobre as cotas
do FIP deve ser mantido. Cole aqui os fólios e a pretensão.
```

```
/metodo-adversarial:premortem-financeiro Valuation: equity do FIP >= R$108M com
base na LOI de ago/2025. Onde o número quebra?
```

Ou descreva: *"blinda essa tese"*, *"como o outro lado vai impugnar"*, *"qual a fragilidade desse valuation"* — a skill correspondente dispara sozinha.

## Guardrails (inscritos em todas as skills)

- **Registro "em tese"** (CF art. 5º, LVII) para caracterização de conduta; sem afirmação categórica de crime/fraude sem trânsito.
- **Suposição não vira fato**: asserção factual com fólio (fls.) ou `[A CONFIRMAR]`; premissa financeira sempre explícita.
- **Steelman honesto**: o argumento contrário é o mais forte possível — espantalho gera falsa segurança.
- **Impugnação sem resposta é registrada, não escondida** — vira pedido de prova, reformulação, ou risco assumido.
- **Output é instrumento interno de trabalho.** Protocolo exige subscrição de advogado(a) (OAB); versão pericial exige profissional habilitado (CRC).
- **Não se manipula o julgador.** O método antecipa objeção e robustece fundamento — não induz, pressiona ou fabrica concessão de quem decide.

## Procedência

As 9 técnicas-origem são o método público de Chris Voss / Black Swan Group (*Never Split the Difference*). O plugin operacionaliza a arquitetura cognitiva, não reproduz texto da obra, e converte a camada de influência em rigor antecipatório aplicável a contexto adversarial legítimo.
