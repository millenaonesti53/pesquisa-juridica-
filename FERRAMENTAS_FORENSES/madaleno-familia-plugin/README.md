# madaleno-familia-plugin

Skill de **mindset jurídico** para Direito de Família patrimonial, inspirada no repertório doutrinário de Rolf Madaleno (advogado, ex-Desembargador do TJRS, professor, um dos fundadores/ex-presidente do IBDFAM, autor do tratado *Direito de Família* e de obra de referência sobre a desconsideração da personalidade jurídica no juízo de família).

## O que a skill faz

Reencaminha a análise de casos de partilha com patrimônio complexo de **"isso é uma questão societária"** para **"isso é comunicabilidade de bens mascarada por engenharia societária"**, através de seis lentes:

1. **Disregard familiarista** — padrão probatório atenuado para desconsideração da personalidade jurídica no contexto de rompimento conjugal.
2. **Sub-rogação real** — rastrear a cadeia de conversões do bem, não debater a validade de cada ato isolado.
3. **Simulação e fraude à meação** — distinguir de fraude à execução; ampliar a janela temporal de ataque a atos suspeitos para toda a constância do casamento.
4. **Dano moral por violência patrimonial** — pedido indenizatório autônomo, distinto da partilha e dos alimentos.
5. **Alimentos compensatórios** — distintos dos alimentos regulares/civis, com fundamento próprio.
6. **Cautelares patrimoniais primeiro** — preservação antes de discussão de mérito sobre valor.

Ver `skills/mindset-dr-madaleno/SKILL.md` (núcleo) e `skills/mindset-dr-madaleno/references/teses-madaleno.md` (síntese doutrinária de apoio).

## Como ativar (requer aprovação do usuário)

Este plugin está **armazenado, não ativado** — mesma política de segurança do restante de `FERRAMENTAS_FORENSES/` (ver README raiz da pasta). Para ativar localmente:

```bash
mkdir -p ~/.claude/plugins
cp -r FERRAMENTAS_FORENSES/madaleno-familia-plugin ~/.claude/plugins/
```

Sem ativação, o conteúdo da skill pode ser lido e aplicado manualmente pelo agente sempre que o usuário pedir para "aplicar o mindset do Madaleno" a uma peça ou análise.

## Verificação de segurança

Conteúdo é 100% markdown/JSON (SKILL.md, references, manifests) — nenhum script executável, nenhuma chamada de rede, nenhuma dependência externa. Autoria declarada: Millena Onesti Gorenstein.

## Reserva metodológica

Doutrina é reforço interpretativo, nunca substitui lei, precedente vinculante verificado ou a subscrição de advogado(a) inscrito(a) na OAB. Nenhuma citação literal de obra específica deve ir a peça protocolável sem conferência direta na fonte.
