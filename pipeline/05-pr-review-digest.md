# Módulo 5 — PR Review Digest

**Pipeline Cognitivo Corporativo | Estágio 5/5**

---

## Função Tecnológica

Consolidar todos os outputs dos módulos anteriores em documentos estruturados:

- Relatórios técnicos para o CLO
- Pareceres jurídicos para o IDPJ
- Minutas para COAF e MPF
- Mapa de ativos penhoráveis

## Função Jurídica

Revisar e enquadrar juridicamente todas as evidências coletadas:

### Enquadramento Penal e Civil

| Diploma | Dispositivo | Conduta Identificada |
|---------|-------------|---------------------|
| Código Penal | Art. 171 | Estelionato — obtenção de vantagem ilícita mediante fraude |
| CPC | Art. 792 | Fraude à execução — alienação de bens após citação |
| Código Civil | Art. 50 | Ocultação patrimonial via abuso da personalidade jurídica |
| Lei 9.613/98 | Arts. 1°-2° | Lavagem de capitais — ocultação de bens de origem ilícita |

## Rotina Integrada

### Documentos Gerados por Ciclo

#### 1. Relatório Final para CLO

```markdown
Estrutura:
  1. Síntese executiva (1 página)
  2. Mapa de ativos identificados
  3. Inconsistências críticas (ranked por valor)
  4. Ações jurídicas recomendadas
  5. Cronograma de próximas providências
```

#### 2. Parecer para IDPJ

Seguir estrutura padrão CLAUDE.md:

```markdown
1. Síntese
2. Fatos (com referência às fontes)
3. Fundamentação jurídica (citações precisas)
4. Conclusão (com recomendações específicas)
```

#### 3. Minuta para COAF / MPF

```markdown
Elementos obrigatórios:
  - Qualificação completa do investigado
  - Descrição das movimentações suspeitas com datas e valores
  - Enquadramento legal (Lei 9.613/98)
  - Pedidos específicos de investigação
  - Documentos anexos
```

#### 4. Mapa de Ativos Penhoráveis

| Ativo | Instituição | Valor Estimado | Status Bloqueio | Penhorabilidade |
|-------|-------------|----------------|-----------------|-----------------|
| FRAM XIV FIP | FRAM | R$ 3.877.255,47 | Ordem enviada (cód. 98) | Contestada — refutar |
| LIG | Itaú | R$ 1.250.000,00 | Esvaziado pós-intimação | Rastrear destino |
| CDB | BTG | R$ 650.758,60 | Saldo zero reportado | Requerer extrato |
| Bonifácio FIP | A identificar | A apurar | Não bloqueado | Bloquear urgente |

### Argumentos para Refutar Impenhorabilidade

#### FIPs — Impenhorabilidade Alegada

A alegação de impenhorabilidade de FIPs deve ser refutada com base em:

1. **Cotas como bem penhorável** — art. 835, IX, CPC: cotas de fundos são bens penhoráveis
2. **Iliquidez não demonstrada** — cabe ao devedor provar a iliquidez; PL positivo a contradiz
3. **Criação pós-litígio** — FIPs criados após a citação são ineficazes perante o credor (art. 792 CPC)
4. **Abuso da personalidade jurídica** — utilização do FIP como escudo patrimonial autoriza desconsideração (art. 50 CC)

#### LIG Itaú — Impenhorabilidade Alegada

Letras Imobiliárias Garantidas (LIG) podem ser penhoradas quando:

1. O devedor é o titular (não o emissor)
2. O vencimento é posterior à penhora (o produto do resgate é penhorável)
3. Há indícios de que a aplicação visou frustrar a execução

### Checklist Final antes de Peticionar

- [ ] Todos os valores confirmados com fonte primária
- [ ] Datas verificadas contra registros CVM e SISBAJUD
- [ ] Números de processo, CNPJs e CPFs verificados (não inventar)
- [ ] Dados sensíveis removidos da versão para protocolo público
- [ ] Enquadramento legal revisado por advogado responsável
- [ ] Assinatura digital do responsável técnico

### Whole Money Trail — Reconstrução

```
Objetivo: rastrear o caminho completo dos recursos desde a origem
          até os veículos atuais de ocultação.

Método:
  1. Identificar fonte primária dos recursos
  2. Mapear cada transferência (data, valor, origem, destino)
  3. Identificar veículos de interposição (FIPs, SPVs, offshore)
  4. Calcular o saldo final e comparar com o débito executado
  5. Identificar beneficiários finais

Status atual: EM CONSTRUÇÃO — ver pesquisas/whole-money-trail.md
```

### Saída Final do Pipeline

- `notas/relatorio-clo-[data].md` — relatório executivo
- `notas/parecer-idpj-[data].md` — parecer jurídico estruturado
- `notas/minuta-coaf-[data].md` — minuta para autoridades
- `pesquisas/mapa-ativos-penhoraveis.md` — mapa atualizado de ativos
- `pesquisas/whole-money-trail.md` — reconstrução do fluxo financeiro
