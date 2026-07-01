# FERRAMENTAS_FORENSES — plugins/skills do caso (armazenados, não ativados)

Esta pasta versiona, no repositório, os plugins/skills do Claude Code construídos para o caso. **Estão armazenados aqui (durável, revisável), NÃO instalados como plugins ativos.**

> **Por que não estão em `.claude/plugins/`?** Instalar plugins com scripts executáveis vindos de upload diretamente no diretório que o agente carrega na inicialização é **auto-modificação** e foi corretamente bloqueado pelo modo de segurança. A ativação exige aprovação explícita da usuária (ver "Como ativar" abaixo).

## Plugins incluídos

### 1. `pesquisa-viva-forense/` (autoria: Millena Onesti Gorenstein)
Trata a pesquisa forense do caso como **ESTADO VIVO**, versionável, com nível probatório por asserção:
- **FATO** = há comprovante nos autos (citável);
- **[CONFERIR]** = asseverado, mas pende certidão/documento;
- **LINHA DE PROVA** = hipótese a confirmar por prova a requerer.
Política cumulativo-expansiva (nunca deleta; promove com motivo). Gera o "Doc 102" (revisão do Doc 101) em PDF/DOCX a partir do estado. Inclui:
- `scripts/pesquisa_ledger.py` — motor de estado (init/list/add/promover/stats/lacunas/export-md);
- `scripts/gerar_dossie.py` — projeta o dossiê (usa `soffice` p/ PDF e `node` + `docx`/`pdf-lib` p/ DOCX);
- `skills/pesquisa-viva-nucleo` e `skills/dossie-saneatorio` (com `references/lacunas-doc101.md` — análise das 7 lacunas do Doc 101);
- `commands/pesquisa.md`, `commands/dossie.md`; `agents/auditor-pesquisa.md`.

### 2. `metodo-adversarial-plugin/` 
Método adversarial / pré-mortem para testar teses antes do protocolo:
- `skills/premortem-tese-juridica`, `skills/premortem-tese-financeira`;
- referências: `advogado-do-diabo.md`, `taxonomia-impugnacao.md`, `taxonomia-objecao.md`, `movimentos.md`.

### 3. `madaleno-familia-plugin/`
Mindset jurídico para Direito de Família patrimonial, inspirado no repertório doutrinário de Rolf Madaleno — seis lentes para casos de partilha com ocultação patrimonial:
- `skills/mindset-dr-madaleno` (disregard familiarista, sub-rogação real, simulação/fraude à meação, dano moral por violência patrimonial, alimentos compensatórios, cautelares patrimoniais primeiro);
- referência: `references/teses-madaleno.md`.
- 100% markdown/JSON — nenhum script executável.

## Dependências (node_modules — NÃO versionado)

O `gerar_dossie.py` usa `node` com os pacotes `docx`, `pdf-lib` e `@pdf-lib/standard-fonts`. O `node_modules` (≈21 MB) **não é versionado** (ver `.gitignore`). Para restaurar:

```bash
npm install -g docx pdf-lib @pdf-lib/standard-fonts
# ou localmente e exportar NODE_PATH para o script encontrar os módulos
```

## Como ativar como plugins (requer aprovação da usuária)

Em ambiente local (fora do modo automático), copiar para o diretório de plugins do Claude Code:

```bash
mkdir -p ~/.claude/plugins
cp -r FERRAMENTAS_FORENSES/pesquisa-viva-forense ~/.claude/plugins/
cp -r FERRAMENTAS_FORENSES/metodo-adversarial-plugin ~/.claude/plugins/
cp -r FERRAMENTAS_FORENSES/madaleno-familia-plugin ~/.claude/plugins/
```

E, se desejar disponibilizá-los ao projeto, mover para `.claude/plugins/` do repositório — decisão da usuária, por envolver execução de código no startup do agente.

## Verificação de segurança (feita)

Conteúdo revisado: markdown (skills/agents/commands), JSON (manifests), Python (ledger/gerador). Os únicos `subprocess` são `soffice --convert-to pdf` e `node` (geração de DOCX) — benignos. Nenhuma chamada de rede, `eval`, `exec`, exclusão recursiva ou ofuscação. Autoria declarada: Millena Onesti Gorenstein.
