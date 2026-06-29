---
name: pesquisa-viva-nucleo
description: "Mantem uma pesquisa juridico-forense como ESTADO VIVO, versionavel e validavel, em vez de um dossie estatico que envelhece. Cada asercao carrega um nivel probatorio (FATO = comprovante nos autos; CONFERIR = asseverado mas pende certidao/documento; LINHA DE PROVA = hipotese a confirmar por prova a requerer), fonte, frente e historico. Politica cumulativo-expansiva: nunca deleta asercao validada, so muda de nivel registrando motivo e data. Gerencia a fila de producao de prova (o que falta para promover cada pendencia a FATO). Use SEMPRE que o usuario quiser atualizar, validar, aprimorar, versionar ou consultar o estado de uma pesquisa/dossie forense, registrar nova asercao ou prova, promover uma asercao quando a prova chega, ou ver o que ainda falta provar. Dispara com 'atualiza a pesquisa', 'valida essa asercao', 'o que falta provar', 'promove para fato', 'registra essa prova', 'estado da pesquisa', 'fila de prova'. Usa scripts/pesquisa_ledger.py. E o nucleo chamado pela skill dossie-saneatorio."
---

# Pesquisa Viva — núcleo de estado probatório

Esta skill resolve um problema estrutural: **um dossiê forense estático envelhece**. No dia em que é escrito, mistura o que já está provado com o que ainda é hipótese; semanas depois, ninguém sabe o que mudou, o que foi confirmado, o que ainda falta. A pesquisa vira um PDF morto que precisa ser reescrito do zero a cada avanço.

A solução é tratar a pesquisa como **estado vivo**: um ledger de asserções, cada uma com seu nível probatório, que evolui à medida que a prova chega. O dossiê passa a ser uma *projeção* do estado num dado momento — regenerável, nunca obsoleto.

## A regra probatória (núcleo do método)

Toda asserção da pesquisa recebe **um de três níveis** — a classificação mista fixada para este caso:

| Nível | Significado | Tratamento |
|---|---|---|
| **FATO** | Há comprovante nos autos: confissão em petição do réu, documento juntado, decisão judicial. | Citável com fls. Sustenta pedido. |
| **[CONFERIR]** | Asseverado nas minutas/no acervo, mas ainda sem certidão ou documento que feche. | Não usar como incontroverso até promover. |
| **LINHA DE PROVA** | Hipótese de investigação; depende de prova a requerer (ofício, exibição, perícia). | Vira pedido de produção de prova no saneamento. |

**Por que isso importa neste litígio:** o erro de tratar hipótese como fato — afirmar categoricamente o que ainda não está provado — é exatamente o vetor de impugnação por má-fé que já foi usado contra material gerado por IA (fls. 2880-2892). O nível probatório é a trava contra esse erro.

## O script é a trava de estado

O agente conversa e analisa; o script `scripts/pesquisa_ledger.py` mantém o estado e impõe a disciplina. Não confie no modelo para "lembrar" o que está provado — registre no ledger.

```
scripts/
  pesquisa_ledger.py   # init | list | add | promover | stats | lacunas | export-md
estado/
  pesquisa.json        # ledger de asercoes (stdlib/JSON, UTF-8)
```

O ledger nasce semeado com o conteudo do Doc 101 + as 7 lacunas identificadas (movimentacoes Apoio->Ari; R$ 5 MM desbloqueados; dicotomia FRAM-iliquido x Itau-liquido; shadow director; rendimentos de fundos no IR; aumento de capital no IR; cruzamento comprovantes x fundos do IR / coinvestimento).

## Operações

### Consultar o estado
```
python3 scripts/pesquisa_ledger.py stats          # contagem por nivel e frente
python3 scripts/pesquisa_ledger.py list --frente patrimonial
python3 scripts/pesquisa_ledger.py list --nivel LINHA_DE_PROVA
```

### Ver o que falta provar (a fila de produção de prova)
```
python3 scripts/pesquisa_ledger.py lacunas
```
Lista só o que ainda não é FATO, com a prova necessária para promover cada item. É a agenda de saneamento: cada LINHA DE PROVA vira um pedido (ofício, exibição, perícia).

### Registrar nova asserção
Quando a pesquisa avança ou surge um achado:
```
python3 scripts/pesquisa_ledger.py add --frente patrimonial --nivel LINHA_DE_PROVA \
  --asercao "..." --fonte "..." --prova-necessaria "..."
```
Frentes: `partilha | pensoes | guarda | transversal | patrimonial`.

### Promover quando a prova chega (validação)
Quando a certidão/documento fecha uma pendência:
```
python3 scripts/pesquisa_ledger.py promover --id AS0004 --para FATO \
  --motivo "Certidao TJMS 0926609-45.2024 juntada fls. XXXX"
```
A política é **cumulativo-expansiva**: a asserção não é apagada nem reescrita — muda de nível, e o histórico registra de/para/motivo/data. Nada validado se perde.

### Regenerar o dossiê
```
python3 scripts/pesquisa_ledger.py export-md > dossie.md
```
Projeta o estado atual como dossiê estruturado (por frente, por nível, com a fila de prova). Sempre atual, porque é gerado do estado.

## Como o agente conduz

- **Usuário traz um achado/prova nova** → classifique no nível certo (tem comprovante nos autos? FATO. Asseverado sem fechar? CONFERIR. Hipótese? LINHA DE PROVA) e registre com `add`.
- **Usuário diz que uma prova chegou** → `promover` com o motivo (a certidão/documento específico).
- **Usuário pergunta "o que falta"** → `lacunas`, e traduza cada pendência no pedido de saneamento correspondente.
- **Usuário quer o dossiê atualizado** → `export-md` e, se pedir formato final, aciona a skill `dossie-saneatorio` (PDF/DOCX).
- **Validação periódica** → reveja os FATO que dependem de certidão ainda não juntada; eles podem precisar voltar a CONFERIR se a fonte se mostrar insuficiente.

## Guardrails

1. **Nível probatório é inviolável.** Hipótese não é fato. O que não tem comprovante nos autos não recebe nível FATO, por mais convincente que pareça.
2. **Cumulativo-expansivo.** Nunca deletar asserção validada; só mudar de nível com motivo registrado.
3. **Fonte obrigatória.** FATO sem fls./Doc é contradição — ou tem fonte, ou não é FATO.
4. **Registro "em tese"** para caracterização de conduta (CF art. 5º, LVII), em qualquer nível.
5. **Atribuição correta:** Kezia (OAB/SP 533.206) = parte adversa; patronos = Hilgenberg (OAB/SC 41.607), Guieseler Junior (OAB/PR 44.937).
6. **UTF-8** explícito; nunca Perl. Saída em português do Brasil.
7. **Não substitui subscrição.** O dossiê é apoio interno; protocolo exige subscrição dos patronos.

Saída sempre em português do Brasil.
