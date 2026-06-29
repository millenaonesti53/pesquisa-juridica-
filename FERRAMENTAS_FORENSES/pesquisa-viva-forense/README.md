# pesquisa-viva-forense

Plugin do Claude Code que mantém a pesquisa jurídico-forense do caso **Onesti × Gorenstein** como **estado vivo** — versionável, validável e regenerável — em vez de um dossiê estático que envelhece.

## O problema que resolve

Um dossiê forense, no dia em que é escrito, mistura o que já está provado com o que ainda é hipótese. Semanas depois, ninguém sabe o que mudou, o que foi confirmado, o que ainda falta. A pesquisa vira um PDF morto, reescrito do zero a cada avanço — e tratar hipótese como fato é exatamente o vetor de impugnação por má-fé já usado neste litígio (fls. 2880-2892).

## A solução

A pesquisa passa a ser um **ledger de asserções**, cada uma com um **nível probatório**:

| Nível | Significado |
|---|---|
| **FATO** | Há comprovante nos autos (confissão em petição, documento, decisão). Citável. |
| **[CONFERIR]** | Asseverado, mas pende certidão/documento que feche. |
| **LINHA DE PROVA** | Hipótese; depende de prova a requerer (ofício, exibição, perícia). |

O dossiê (Doc 102) é uma **projeção** desse estado — sempre atual, porque é gerado do ledger.

## Componentes

**Skills**
- `pesquisa-viva-nucleo` — o método de manter a pesquisa viva; opera o ledger.
- `dossie-saneatorio` — gera o Doc 102 em PDF (identidade visual do Doc 101) + DOCX editável.

**Comandos**
- `/pesquisa` — consulta/atualiza o estado (o que falta, registrar achado, promover quando a prova chega).
- `/dossie` — gera/regenera o Doc 102 nos dois formatos.

**Agente**
- `auditor-pesquisa` — revisa fragilidades probatórias (FATO sem lastro, linha de prova sem pedido, contradições).

**Scripts**
- `scripts/pesquisa_ledger.py` — motor de estado (init · list · add · promover · stats · lacunas · export-md).
- `scripts/gerar_dossie.py` — gera o Doc 102 (PDF via WeasyPrint; DOCX via docx-js; fallback soffice).

**Estado**
- `estado/pesquisa.json` — o ledger (semeado com o Doc 101 + as 7 lacunas).

## As 7 lacunas integradas (que faltavam no Doc 101)

1. Movimentações Apoio Adm. → Ari (fluxo Evino→Apoio Adm.→PF)
2. R$ 5 MM desbloqueados indevidamente sobre ativo localizado como líquido
3. Dicotomia: cotas FRAM/Ajaccio ilíquidas *sem documento* × Itaú R$ 10 MM líquido
4. Shadow director: controle fático da Evino + salário Vila Porto + diretor de novos negócios
5. Rendimentos de fundos declarados no IR (contra a alegação de "receita zero")
6. Aumento de capital no IR (contra a narrativa de perda de renda)
7. Cruzamento comprovantes × fundos do IR (coinvestimento / fundo de fundos)

## Uso rápido

```bash
# inicializa o estado (semente: Doc 101 + 7 lacunas)
python3 scripts/pesquisa_ledger.py init

# o que ainda falta provar
python3 scripts/pesquisa_ledger.py lacunas

# quando a prova chega
python3 scripts/pesquisa_ledger.py promover --id AS0004 --para FATO \
  --motivo "Certidao TJMS juntada fls. XXXX"

# gera o Doc 102 (PDF + DOCX)
python3 scripts/gerar_dossie.py
```

## Instalação

```
/plugin marketplace add ./pesquisa-viva-forense
/plugin install pesquisa-viva-forense@marketplace-forense-gorenstein
```

## Princípios

- **Nível probatório é inviolável** — hipótese não é fato.
- **Cumulativo-expansivo** — nunca deletar asserção validada; só promover com motivo registrado.
- **O documento projeta o estado** — corrigir conteúdo é corrigir o ledger e regenerar.
- **Não substitui subscrição** — todo Doc 102 sai marcado NÃO PROTOCOLAR SEM SUBSCRIÇÃO, com os patronos nomeados (Hilgenberg OAB/SC 41.607; Guieseler Junior OAB/PR 44.937).

Registro "em tese" (CF art. 5º, LVII). UTF-8; nunca Perl. Português do Brasil.
