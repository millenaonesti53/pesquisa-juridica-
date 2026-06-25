# Módulo 3 — 🔄 Dependency Update Check

**Pipeline Cognitivo Corporativo | Estágio 3/5 | v2.0**

---

## Visão Geral

Mantém todas as bases de dados atualizadas e detecta alterações estruturais suspeitas em veículos patrimoniais. Cada atualização é comparada com o estado anterior para identificar mudanças com potencial jurídico relevante.

---

## Função Tecnológica

Atualizar bases e detectar mudanças relevantes:

| Fonte | Periodicidade | Tipo de Dado | Acesso |
|-------|--------------|--------------|--------|
| CVM | Diária | FIPs, PLs, regulamentos, classes de cotas | API pública CVM |
| Receita Federal | Semanal | IRPF, CNPJ, vínculos societários | Portal e cruzamento |
| Bancos (SISBAJUD) | Por demanda | Extratos, saldos, histórico | SISBAJUD |
| FATCA/CRS | Mensal | Ativos e contas internacionais | Relatórios IRS/OCDE |
| Registros de FIPs | Diária | Cotas, cotistas, regulamento vigente | CVM EDGAR |

---

## Função Jurídica

Identificar alterações estruturais suspeitas em veículos patrimoniais:

1. **Criação retroativa de classes** — ex.: Classe J criada após o início do litígio para isolar ativos
2. **Side-pockets** — segregação de ativos ilíquidos sem justificativa econômica legítima
3. **Alterações de regulamento** — mudanças que dificultem bloqueio, penhora ou alienação
4. **Cisões e SPVs novas** — criação de Sociedades de Propósito Específico após a ação judicial
5. **Participações cruzadas** — verificar se os mesmos administradores/gestores controlam múltiplos FIPs investigados

---

## Rotina Integrada

### Casos Identificados

#### Bonifácio FIP — Criação Pós-Litígio

```
Status: ALERTA CRÍTICO

Fato:      FIP criado após o início do litígio
Hipótese:  Veículo constituído para receber e ocultar ativos do devedor
Base:      Art. 792, IV, CPC — ineficácia de atos pós-citação
           Art. 50, CC — desconsideração da personalidade jurídica

Ações:
  → Solicitar documentação constitutiva completa via CVM
  → Identificar CNPJ, administrador e gestor
  → Verificar cotistas e aportes após a citação judicial
  → Cruzar cotistas com o CPF/CNPJ do devedor e seus associados
```

#### FRAM XIV — Side-Pocket Suspeito

```
Status: ALERTA ALTO

Fato:      Existência de side-pocket no FRAM XIV FIP
PL atual:  R$ 3.877.255,47
Hipótese:  Segregação de ativos líquidos para proteção indevida;
           iliquidez alegada contradiz o PL positivo
Base:      Art. 835, IX, CPC — cotas de fundos são penhoráveis
           Iliquidez deve ser demonstrada pelo devedor (STJ)

Ações:
  → Requerer demonstrações financeiras completas
  → Solicitar laudo de avaliação do side-pocket
  → Questionar a justificativa econômica da segregação
```

#### Bonifácio — Classe J Criada Pós-Litígio

```
Status: ALERTA CRÍTICO

Fato:      Classe J de cotas criada após o início do litígio
Hipótese:  Tentativa de criar compartimento "protegido" para
           isolar ativos da ação de execução
Base:      Art. 792, IV, CPC — ineficácia perante o credor
           Criação fraudulenta invalida a proteção alegada

Ação:
  → Requerer ao juízo declaração de ineficácia da Classe J
  → Documentar a cronologia: data da citação × data de criação
```

#### Ajaccio — Inconsistência Temporal

```
Status: ALERTA ALTO

Fato:      Inconsistência temporal identificada no Ajaccio
Hipótese:  Data de operação incompatível com a cronologia declarada;
           possível antedatação ou simulação
Base:      Art. 167, CC — nulidade do negócio simulado

Ações:
  → Cruzar datas com registros CVM e extratos bancários
  → Confrontar com IRPF dos anos correspondentes
  → Solicitar documentação original com reconhecimento de firma ou carimbo
```

---

## Checklist de Verificação — Ciclo Diário

- [ ] Comparar regulamento atual × regulamento na data da citação
- [ ] Verificar se houve emissão/resgate de cotas após o bloqueio
- [ ] Identificar cotistas atuais vs. cotistas na data da penhora
- [ ] Checar CNPJs de administradoras e gestoras por vínculos com o devedor
- [ ] Verificar participações cruzadas entre FIPs monitorados
- [ ] Atualizar PL de todos os FIPs com dados CVM mais recentes
- [ ] Verificar novos registros de FIPs com cotistas vinculados ao devedor
- [ ] Cruzar IRPF mais recente × posição de ativos CVM + SISBAJUD

---

## Saída do Módulo

- Log de dependências atualizadas (técnico)
- **Relatório de alterações suspeitas** → alimenta Módulo 4 (Flaky Tracker)
- Notificações para o time jurídico sobre eventos com relevância processual

---

## Legislação de Referência

- Art. 50, CC — Desconsideração da personalidade jurídica
- Art. 167, CC — Nulidade do negócio jurídico simulado
- Art. 792, IV, CPC — Fraude à execução (atos pós-citação)
- Art. 835, IX, CPC — Penhorabilidade de cotas de fundos
- Lei 9.613/98, Art. 1° — Lavagem de capitais (ocultação por veículos)
