---
description: Consulta ou atualiza o estado vivo da pesquisa forense (ledger de asercoes por nivel probatorio)
---

Voce vai operar o estado vivo da pesquisa do caso Onesti x Gorenstein usando a skill `pesquisa-viva-nucleo` e o script `scripts/pesquisa_ledger.py`.

Pedido do usuario: $ARGUMENTS

Roteiro:
1. Se o ledger ainda nao existe, rode `python3 scripts/pesquisa_ledger.py init` (cria a semente: Doc 101 + 7 lacunas).
2. Interprete a intencao:
   - **Consultar** ("o que falta", "estado", "mostra as linhas de prova") -> use `stats`, `list --frente X`, `list --nivel Y` ou `lacunas`.
   - **Registrar achado novo** -> classifique no nivel certo (tem comprovante nos autos? FATO; asseverado sem fechar? CONFERIR; hipotese? LINHA_DE_PROVA) e use `add`.
   - **Prova chegou** ("promove AS00XX", "ja temos a certidao") -> use `promover --id ... --para ... --motivo ...`.
3. Ao registrar/promover, confirme a operacao e mostre o `stats` atualizado.
4. Traduza cada LINHA DE PROVA pendente no pedido de saneamento correspondente (oficio, exibicao, pericia) quando o usuario perguntar "o que falta".

Regras: nivel probatorio e inviolavel (hipotese != fato); politica cumulativo-expansiva (nunca deletar, so promover com motivo); fonte obrigatoria em FATO; "em tese" para conduta; Kezia = parte adversa; patronos = Hilgenberg (OAB/SC 41.607) e Guieseler Junior (OAB/PR 44.937). Portugues do Brasil.
