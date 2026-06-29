# Módulo 3 — Dependency Update Check

**Pipeline Cognitivo Corporativo | Estágio 3/5**

---

## Função Tecnológica

Manter as bases de dados atualizadas e detectar mudanças relevantes:

- Bases CVM — FIPs, fundos, PL, regulamentos
- Extratos bancários — novos documentos recebidos
- IRPF — declarações e atualizações
- Logs FATCA/CRS — obrigações internacionais de transparência
- Dados estruturais de FIPs — cotas, classes, regulamentos

## Função Jurídica

Identificar alterações estruturais suspeitas em veículos patrimoniais:

1. **Criação retroativa de classes** — ex.: criação da Classe J após início do litígio
2. **Side-pockets** — segregação de ativos ilíquidos sem justificativa econômica
3. **Alterações de regulamento** — mudanças que dificultem a penhora ou reduzam o PL nominal
4. **Cisões e SPVs novas** — criação de Sociedades de Propósito Específico pós-ação judicial

## Rotina Integrada

### Fontes e Periodicidade

| Fonte | Periodicidade | Tipo de Dado | API/Acesso |
|-------|--------------|--------------|------------|
| CVM | Diária | FIPs, PLs, regulamentos | API pública CVM |
| Receita Federal | Semanal | IRPF, CNPJ | Portal |
| Bancos (SISBAJUD) | Por demanda | Extratos, saldos | SISBAJUD |
| FATCA/CRS | Mensal | Ativos internacionais | Relatórios IRS/OCDE |

### Casos Identificados

#### Bonifácio FIP — Criação Pós-Litígio

```
Status: ALERTA CRÍTICO
Fato: FIP criado após o início do litígio
Hipótese: veículo constituído para receber/ocultar ativos do devedor
Enquadramento: art. 50 CC (desconsideração PJ) + art. 792 CPC (fraude à execução)
Ação: solicitar documentação constitutiva completa + CNPJ + administrador
```

#### FRAM XIV — Side-Pocket Suspeito

```
Status: ALERTA ALTO
Fato: existência de side-pocket no FRAM XIV FIP
Hipótese: segregação de ativos líquidos para proteção indevida
Enquadramento: iliquidez alegada vs. PL real de R$ 3.877.255,47
Ação: requerer demonstrações financeiras completas + laudo de avaliação
```

#### Ajaccio — Inconsistência Temporal

```
Status: ALERTA ALTO
Fato: inconsistência temporal identificada no Ajaccio
Hipótese: data de operação incompatível com cronologia declarada
Enquadramento: fraude documental / simulação (art. 167 CC)
Ação: cruzar datas com registros CVM e extratos bancários
```

### Checklist de Verificação

- [ ] Comparar regulamento atual × regulamento na data da citação
- [ ] Verificar se houve emissão/resgate de cotas após bloqueio
- [ ] Identificar cotistas atuais vs. cotistas na data da penhora
- [ ] Checar CNPJs de administradoras e gestoras por vínculos com o devedor
- [ ] Verificar se há participações cruzadas entre FIPs monitorados
- [ ] Verificar logs FATCA/CRS para ativos internacionais não declarados

### Saída
- Log de dependências atualizadas
- Relatório de alterações suspeitas (alimenta Flaky Tracker)
- Notificações para o time jurídico sobre eventos relevantes
