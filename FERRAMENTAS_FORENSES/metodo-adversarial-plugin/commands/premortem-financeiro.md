---
description: Submete uma tese financeira/contabil (valuation, apuracao de haveres, rastreamento patrimonial, parecer) ao pre-mortem adversarial — steelman do avaliador adverso, auditoria de objecao tecnica com sensibilidade, e traducao em parecer Diagnostico-Evidencia-Implicacoes-Cenarios-Estrategia-Acao. Aciona a skill premortem-tese-financeira.
argument-hint: [cole o laudo/calculo/tese, ou descreva o ativo e a pretensao de valor]
---

Acione a skill **premortem-tese-financeira** (`skills/premortem-tese-financeira/SKILL.md`), que chama o núcleo **metodo-adversarial-nucleo**.

Entrada do usuário: $ARGUMENTS

Roteiro:

1. **Leia** a skill financeira, o núcleo (`metodo-adversarial-nucleo/SKILL.md`) e os arquivos de referência (`movimentos.md` e `taxonomia-objecao.md`) antes de produzir qualquer análise.
2. **Calibre o ponto de entrada:**
   - Valuation/laudo colado com contexto suficiente → vá direto a Fase 2 (steelman do avaliador adverso) + Fase 3 (auditoria de objeção técnica com sensibilidade) + Fase 4 (cenários).
   - Construção do zero → comece na Fase 1.
   - Só pré-mortem técnico → Fases 2-4, sem redigir parecer.
3. **Produza o ciclo** com cada movimento marcado entre colchetes (`[STEELMAN]`, `[AUDITORIA]`, `[NOMEACAO]`, `[SOBRIO]`).
4. **Steelman honesto**: reconstrua o melhor parecer divergente possível — ataque premissa, método e dado no ponto mais forte.
5. **Sensibilidade obrigatória** para premissa-chave: mostre como o resultado muda sob a premissa adversa; entregue faixa, não ponto único. Declare os limites do método.
6. Se desembocar em parecer, estruture Diagnóstico → Evidência → Implicações → Cenários → Estratégia → Ação. Antes de qualquer planilha de suporte, rode `recalc.py`; campos-resumo oficiais são as totalizações autoritativas; Python com encoding explícito (nunca Perl em UTF-8). Carimbe: **"INSTRUMENTO INTERNO DE TRABALHO — NÃO PROTOCOLAR. Versão pericial exige subscrição de profissional habilitado (CRC)."**
7. Caracterização de conduta (distribuição disfarçada, esvaziamento, fraude) em registro "em tese".
8. Ao final, ofereça o teste de convicção via agente `advogado-do-diabo` (que opera também como perito-contador adverso).
