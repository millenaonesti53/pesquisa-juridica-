# Módulo 5 — 🔍 PR Review Digest

**Pipeline Cognitivo Corporativo | Estágio 5/5 | v2.0**

---

## Visão Geral

Consolida todos os outputs dos módulos anteriores em documentos estruturados prontos para uso jurídico: relatórios para o CLO, pareceres para o IDPJ, minutas para COAF/MPF e o mapa de ativos penhoráveis atualizado.

---

## Função Tecnológica

Consolidar e estruturar os outputs do pipeline:

- Relatórios técnicos para o CLO (Chief Legal Officer)
- Pareceres jurídicos para o IDPJ
- Minutas para COAF e MPF
- Mapa atualizado de ativos penhoráveis
- Reconstrução do Whole Money Trail

---

## Função Jurídica

Revisar e enquadrar juridicamente todas as evidências coletadas:

### Enquadramento Penal e Civil

| Diploma | Dispositivo | Conduta Identificada |
|---------|-------------|---------------------|
| Código Penal | Art. 171 | Estelionato — obtenção de vantagem ilícita mediante fraude |
| CPC | Art. 792 | Fraude à execução — alienação/esvaziamento de bens após citação |
| CPC | Art. 774 | Atos atentatórios à dignidade da justiça (não resposta ao SISBAJUD) |
| Código Civil | Art. 50 | Ocultação patrimonial via abuso da personalidade jurídica |
| Código Civil | Art. 167 | Nulidade do negócio jurídico simulado |
| Lei 9.613/98 | Arts. 1°-2° | Lavagem de capitais — ocultação de bens de origem ilícita |
| CPC | Art. 835, IX | Penhorabilidade de cotas de fundos de investimento |

---

## Rotina Integrada

### Documentos Gerados por Ciclo

#### 1. Relatório Final para CLO

```markdown
Estrutura:
  1. Síntese executiva (1 página)
  2. Mapa de ativos identificados (tabela com valor, status, risco)
  3. Inconsistências críticas (rankadas por valor e urgência)
  4. Padrões de comportamento suspeito (flakiness detectada)
  5. Ações jurídicas recomendadas (com base legal)
  6. Cronograma de próximas providências

Arquivo de saída: notas/relatorio-clo-[AAAA-MM-DD].md
```

#### 2. Parecer para IDPJ

Estrutura padrão (per CLAUDE.md):

```markdown
1. Síntese
   Resumo do estado patrimonial investigado e das inconsistências identificadas.

2. Fatos
   Descrição objetiva dos eventos com datas, valores e fontes primárias.
   Referência cruzada: CVM, SISBAJUD, IRPF, extratos.

3. Fundamentação Jurídica
   Citações precisas dos dispositivos legais aplicáveis.
   Jurisprudência relevante (apenas acórdãos verificados).

4. Conclusão
   Recomendações específicas com ações e prazos.

Arquivo de saída: notas/parecer-idpj-[AAAA-MM-DD].md
```

#### 3. Minuta para COAF / MPF

```markdown
Elementos obrigatórios:
  - Qualificação completa do investigado (CPF/CNPJ verificados)
  - Descrição das movimentações suspeitas com datas e valores exatos
  - Identificação das instituições envolvidas
  - Enquadramento legal (Lei 9.613/98)
  - Pedidos específicos de investigação
  - Lista de documentos anexos

Arquivo de saída: notas/minuta-coaf-[AAAA-MM-DD].md
```

#### 4. Mapa de Ativos Penhoráveis (atualizado)

| Ativo | Instituição | Valor Estimado | Status Bloqueio | Impenhorabilidade Alegada | Refutação |
|-------|-------------|----------------|-----------------|--------------------------|-----------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Ordem enviada — cód. 98 | Iliquidez do fundo | PL positivo; art. 835, IX CPC |
| LIG | Itaú | R$ 1.250.000,00 | Esvaziado pós-intimação | A verificar | Rastrear + art. 792 CPC |
| CDB | BTG | R$ 650.758,60 | Saldo zero reportado | — | Art. 774 CPC; requerer extrato |
| Bonifácio FIP | A identificar | A apurar | Não bloqueado | Criação pós-litígio ineficaz | Art. 792, IV CPC |
| Conta Itaú | Itaú | R$ 5.491 (remanescente) | — | — | Rastrear transferências |

**Total identificado:** R$ 5.778.014,07 + Bonifácio FIP (a apurar)

Arquivo de saída: `pesquisas/mapa-ativos-penhoraveis.md` (versão atualizada)

---

## Argumentos para Refutar Impenhorabilidade

### FIPs — Impenhorabilidade Alegada

1. **Cotas como bem penhorável** — art. 835, IX, CPC: cotas de fundos são expressamente penhoráveis
2. **Iliquidez não demonstrada** — cabe ao devedor provar a iliquidez; PL positivo a contradiz
3. **Criação pós-litígio** — FIPs criados após a citação são ineficazes perante o credor (art. 792, IV, CPC)
4. **Abuso da personalidade jurídica** — uso do FIP como escudo patrimonial autoriza desconsideração (art. 50, CC)
5. **Distribuição de rendimentos** — se há distribuição, há fluxo penhorável independente da iliquidez

### LIG Itaú — Titular vs. Emissora

1. O devedor é titular (não emissora) da LIG — logo, é um ativo, não uma obrigação
2. O produto do resgate no vencimento é penhorável (art. 835, IX, CPC)
3. Esvaziamento após intimação configura fraude à execução (art. 792, CPC)
4. Os recursos transferidos devem ser rastreados e bloqueados no destino

### CDB BTG — Inconsistência da Resposta

1. CDB registrado em R$ 650.758,60 — saldo zero inconsistente sem extrato comprobatório
2. Declaração ao SISBAJUD é declaração de verdade sob responsabilidade institucional
3. Se falsa: art. 774, CPC — ato atentatório à dignidade da justiça; representação ao BCB

---

## Whole Money Trail — Reconstrução

```
Objetivo: rastrear o caminho completo dos recursos desde a origem
          até os veículos atuais de ocultação.

Etapas:
  1. Identificar fonte primária dos recursos (atividade, herança, operação)
  2. Mapear cada transferência (data, valor, instituição de origem, destino)
  3. Identificar veículos de interposição (FIPs, SPVs, contas offshore)
  4. Calcular saldo final e comparar com o débito executado
  5. Identificar UBOs — Ultimate Beneficial Owners

Status: EM CONSTRUÇÃO — ver pesquisas/whole-money-trail.md
```

---

## Checklist Final antes de Peticionar

- [ ] Todos os valores confirmados com fonte primária (CVM, SISBAJUD, extrato)
- [ ] Datas verificadas contra registros CVM e SISBAJUD (não inferidas)
- [ ] Números de processo, CNPJs e CPFs verificados — nunca inventar
- [ ] Dados sensíveis (CPF, patrimônio pessoal) removidos da versão pública
- [ ] Enquadramento legal revisado pelo advogado responsável
- [ ] Jurisprudência citada verificada — número de acórdão real
- [ ] Assinatura digital do responsável técnico aplicada

---

## Saídas Finais do Pipeline

| Documento | Destinatário | Arquivo |
|-----------|-------------|---------|
| Relatório executivo | CLO | `notas/relatorio-clo-[data].md` |
| Parecer jurídico | IDPJ | `notas/parecer-idpj-[data].md` |
| Minuta de representação | COAF / MPF | `notas/minuta-coaf-[data].md` |
| Mapa de ativos | Uso interno / juízo | `pesquisas/mapa-ativos-penhoraveis.md` |
| Whole Money Trail | Uso interno / peritos | `pesquisas/whole-money-trail.md` |

---

## Legislação de Referência

- Art. 50, CC — Desconsideração da personalidade jurídica
- Art. 167, CC — Nulidade por simulação
- Art. 171, CP — Estelionato
- Art. 774, CPC — Atos atentatórios à dignidade da justiça
- Art. 792, CPC — Fraude à execução
- Art. 835, IX, CPC — Penhorabilidade de cotas de fundos
- Lei 4.595/64 — Supervisão do BCB
- Lei 9.613/98 — Lavagem de capitais
