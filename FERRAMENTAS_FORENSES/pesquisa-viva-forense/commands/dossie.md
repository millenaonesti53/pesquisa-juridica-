---
description: Gera ou regenera o Doc 102 (dossie saneatorio revisado) em PDF e DOCX a partir do estado vivo
---

Voce vai gerar o Doc 102 usando a skill `dossie-saneatorio` e o script `scripts/gerar_dossie.py`.

Pedido do usuario: $ARGUMENTS

Roteiro:
1. Confirme que o ledger esta atual: `python3 scripts/pesquisa_ledger.py stats`. Se nao existir, rode `init`.
2. Se o usuario indicou que algo mudou na pesquisa, atualize o ESTADO primeiro (via `/pesquisa` ou o script `add`/`promover`) — o documento projeta o estado, entao o estado vem antes.
3. Gere:
   - padrao (os dois formatos): `python3 scripts/gerar_dossie.py`
   - so PDF: `--pdf` · so DOCX: `--docx`
4. Apresente os arquivos gerados com present_files. O PDF tem a identidade visual do Doc 101; o DOCX e editavel para os patronos.

Nunca edite o PDF/DOCX a mao para corrigir conteudo — corrija no ledger e regenere. Todo Doc 102 sai marcado NAO PROTOCOLAR SEM SUBSCRICAO, patronos nomeados. "Em tese" para conduta. Portugues do Brasil.
