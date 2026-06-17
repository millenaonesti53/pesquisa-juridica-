# Nota Técnica — Códigos SISBAJUD por Instituição (2023 × 2026)

> Análise sob a ótica de doutorado em sistemas financeiros. Versão **2** — incorpora a validação cruzada com a planilha Gorenstein e corrige três imprecisões da v1.

**Autos:** proc. 1006744-58.2023 (família) e 0005199-67.2023 + execução 2026.
**Investigado:** Ari Gorenstein, CPF 136.447.108-64.

---

## 1. Síntese

A não repetição de uma instituição na remessa SISBAJUD de 2026 **não é erro nem sumiço probatório**. Tem **três causas técnicas distintas**, mutuamente excludentes na origem, mas frequentemente confundidas na leitura leiga:

1. **Não inclusão na remessa** (a instituição simplesmente não foi consultada);
2. **Mudança do rol de participantes do SFN** (IPs novas surgiram entre 2023 e 2026, e os dois bloqueios são de processos distintos);
3. **Mudança real da situação patrimonial** (o relacionamento existe, mas o status mudou: 32 → 02 → 00).

Cada causa exige resposta processual diferente. A confusão entre elas tem custo concreto.

**Distinção metodológica decisiva (correção em relação a versões anteriores):** comparar código a código entre uma **REQUISIÇÃO de informações** (códigos 30/32/35, fls. 418) e um **BLOQUEIO** (códigos 00/02/03/12/13/25/26, fls. 490/500/123/131) é **metodologicamente incorreto** — são instrumentos com propósitos distintos.

## 2. Fatos (extraídos dos autos validados)

- **2023 — Requisição (fls. 418):** saldo informado consolidado de **R$ 84.856.714,65**.
  - **FRAM Capital DTVM** retornou (98) e depois (32) com **R$ 77.640.365,33**.
  - N26 SCD e BEXS Câmbio retornaram (98) duas vezes (não-resposta).
  - Itaú, BTG, C6, NU, MercadoPago, Santander, XP retornaram (32) com saldos diversos (incluindo zero).
- **2023 — Bloqueio (fls. 490/500):** total bloqueado **R$ 52.932.655,22**.
  - **BTG Pactual:** código (26) — R$ 42.428.357,32 em ativo de baixa liquidez, com remanescente R$ 3.058.369,42.
  - **Itaú Unibanco:** código (13) — transferência de R$ 7.444.483,08 em VM (carta fls. 508/558).
  - **FRAM Capital DTVM:** código (98) — não-respondeu ao bloqueio; reiteração consta como "não enviada".
  - **N26 SCD:** (98) Não-Resposta.
- **2026 — Bloqueio (fls. 123/131):** total bloqueado **R$ 83.752,42** — queda de **−99,8%** em relação a 2023.
  - **OSLO Capital DTVM** surge como custodiante: (25) R$ 27.799,79 em ativo escriturado (depois desbloqueado em 15/04).
  - **BTG:** (12) R$ 27.799,79 em depósito a prazo.
  - **Itaú:** (12) R$ 27.799,79.
  - **FRAM:** ausente da remessa.
  - **N26 SCD** e **BEXS Câmbio:** ausentes da remessa.

Detalhe completo: `pesquisas/sisbajud-cruzamento-instituicoes-2023x2026.csv` e `pesquisas/sisbajud-planilha-explicativa.xlsx` (aba 2).

## 3. Fundamentação

### 3.1 Dicionário dos códigos (redação SISBAJUD)

| Código | Significado | Há ativo? | Natureza da ordem |
|---|---|---|---|
| 00 | Sem relacionamento / contas inativas / não custodia | Não | Bloqueio |
| 01 | Cumprida integralmente | — | Transf./Desbloqueio |
| 02 | Réu/executado sem saldo positivo (é cliente) | Não (conta existe) | Bloqueio |
| 03 | Cumprida parcialmente por insuficiência | Sim (pouco) | Bloqueio |
| 12 | Cumprida integralmente em depósito a prazo | Sim | Bloqueio |
| 13 | Cumprida parcialmente em VM / depósito a prazo | Sim | Bloqueio |
| 16 | Cumprida em outra empresa do grupo | Sim (no grupo) | Bloqueio |
| 25 | Ativo escriturado sem comando de venda | Sim | Bloqueio |
| 26 | Ativo de baixa liquidez | Sim | Bloqueio |
| 30 | Sem as informações requisitadas | Indeterminado | Requisição |
| 32 | Cumprida com as informações existentes | Sim/zero (informa saldo) | Requisição |
| 35 | Cliente inativo / não cliente | Não | Requisição |
| 98 | **Não-Resposta** (silêncio) | Indeterminado | Ambas |

Tabela completa em `pesquisas/sisbajud-dicionario-codigos.csv`.

### 3.2 Por que um código **não se repete** em 2026 — análise das três causas

#### Causa 1 — Instituição não foi reincluída na remessa
O SISBAJUD opera por **lista positiva**: só consulta as instituições explicitamente incluídas pelo juízo. Se a FRAM (que retornou 32/R$ 77,6 Mi em 2023) **não consta** em 2026, isso significa apenas que não foi consultada. A ausência **não é prova de inexistência de ativo** — ao contrário, dado o histórico, é forte indício de que o ativo permanece e ficou invisível à ordem.

> **Consequência processual:** exigir nova ordem com rol completo — mínimo: todas as instituições com código ≠ 00/35 em qualquer das datas anteriores, mais as DTVMs com histórico de coinvestimento.

#### Causa 2 — Lista de participantes do SFN mudou e os processos são distintos
Entre 2023 e 2026, novas Instituições de Pagamento entraram em operação (RecargaPay, 99Pay, Shopee, PicPay, Revolut, Magalu Pagamentos). Além disso, os dois bloqueios são de **processos distintos com valores distintos** (2023: ordem família ~R$ 42,4 mi; 2026: execução ~R$ 27,8 mil). Aparecimento dessas IPs apenas em 2026 não permite inferência sobre 2023.

> **Consequência processual:** justifica ampliar a próxima ordem para incluir todas as IPs registradas no BACEN; é causa **benigna**, não indica blindagem.

#### Causa 3 — Mudança real da situação patrimonial
Quando a **mesma instituição** retorna códigos diferentes nas duas datas, há mudança real:
- **32 → 02:** havia saldo informado, agora não há (zerou);
- **(26) R$ 42 Mi → (12) R$ 27 mil:** queda brutal (BTG) — núcleo da tese de esvaziamento;
- **(13) R$ 7,44 Mi → (12) R$ 27 mil:** Itaú — mesma dinâmica.

> **Consequência processual:** **é aqui** que mora o indício de esvaziamento patrimonial. Para cada transição relevante, pedir **extrato dos 12 meses anteriores ao bloqueio**, com identificação de TED/PIX/transferências de saída acima de R$ 10 mil.

### 3.3 Hierarquia interpretativa dos códigos

Para fins de mapeamento patrimonial em ação de partilha/execução, a **riqueza informacional** dos códigos segue a ordem:

```
32 > 13 ≈ 26 > 25 > 12 > 03 > 16 > 02 > 35 > 00 > 30 > 98
```

- **32** é o mais informativo — revela saldo (positivo ou zero) e confirma relacionamento;
- **98** é o mais sensível — exige reiteração obrigatória;
- **00** é o mais barato em prova, mas o mais armadilhoso quando antecedido de 32 (encerramento ≠ inexistência).

### 3.4 Leitura das instituições críticas

| Instituição | Causa predominante | Diagnóstico |
|---|---|---|
| **FRAM Capital DTVM** | Causa 1 (não reincluída) | **Maior lacuna probatória** — R$ 77,6 Mi reconhecidos em (32) inexplicados em 2026 |
| **OSLO Capital DTVM** | Surgimento novo | Indício de **migração FRAM → OSLO** — investigar |
| **N26 SCD** | Causa 1 + (98) silêncio | Canal de coinvestimento internacional suspeito |
| **BEXS Câmbio** | Causa 1 + (98) silêncio | Mesma dinâmica da N26 |
| **BTG Pactual** | Causa 3 (de R$ 42,4 Mi para R$ 27,8 mil) | Verificar destino dos resgates |
| **Itaú Unibanco** | Causa 3 (de R$ 7,44 Mi VM para R$ 27,8 mil) | Idem |
| **C6 / NU / MercadoPago** | Causa 3 (saldo migalha) | Baixa relevância, mas confirma persistência |

## 4. Conclusão

1. **Não houve falha do SISBAJUD em 2023.** O código (32) da FRAM revelou R$ 77,6 Mi na **REQUISIÇÃO**, e o (26) do **BTG** revelou R$ 42,4 Mi no **BLOQUEIO** — base sólida para o mapeamento patrimonial.

2. **A "não repetição" de códigos em 2026 decorre principalmente de mudança de escopo das ordens** (FRAM/N26/BEXS não reincluídas; processos distintos) e, em parte, de **mudança real do patrimônio** (queda de R$ 52,9 Mi → R$ 83,7 mil = **−99,8%**).

3. **Lacunas críticas a fechar imediatamente:**
   - **FRAM** (ausente em 2026 após R$ 77,6 Mi em 2023) — REINCLUIR;
   - **N26** (silêncio nas duas ordens de 2023, ausente em 2026) — REINCLUIR + ofício individualizado;
   - **BEXS Câmbio** (silêncio em 2023, ausente em 2026) — REINCLUIR;
   - **OSLO** (surge em 2026) — pedir histórico desde 2022 e cruzar fluxo com FRAM;
   - **Itaú/BTG** — pedir **extrato 12 meses anteriores ao bloqueio de 2026**.

### Recomendações técnicas para a próxima ordem

1. **Requisição de Informações ampla (sem valor) ANTES do bloqueio** — para mapear sem alertar movimentações;
2. **Rol expresso obrigatório**: FRAM, OSLO, N26, BEXS, Ajaccio, Bonifácio, todas as IPs ativas e todas as DTVMs com relacionamento prévio;
3. **Reiteração automática** para todo código (98) com prazo de 5 dias e cominação;
4. **Detalhamento por CNPJ de fundo** nas DTVMs — código (32) puro não basta; pedir carteira;
5. **Ofício concentrado à CVM e B3** para os códigos (25) e (26) (ativo escriturado / baixa liquidez);
6. **Pedido de extrato 12 meses** sempre que houver transição 32 → 02 ou 32 → 00 com valor anterior > R$ 10 mil.

---

## 5. Validação e correções (v2)

A v1 desta nota continha três imprecisões corrigidas após cruzamento com a planilha Gorenstein:

| Item | v1 (incorreta) | v2 (validada) | Fonte |
|---|---|---|---|
| Atribuição do código (26) | "FRAM = R$ 31,9 Mi baixa liquidez" | **BTG = R$ 42.428.357,32 → remanescente R$ 3.058.369,42** | fls. 492 |
| Resposta da FRAM no bloqueio 2023 | "(26) R$ 31,9 Mi" | **(98) Não-Resposta** | fls. 493 |
| Valor "R$ 31,9 Mi" | Atribuído à FRAM | **Não consta em nenhum documento** — alucinação removida | n/a |

Confirmações:
- N26 e BEXS: (98) Não-Resposta em ambas as ordens de 2023 (fls. 418, 490, 500)
- C6 R$ 20,90 / NU R$ 72,22 / MercadoPago R$ 218,02 — todos código (32) na requisição
- Total bloqueado 2023: R$ 52.932.655,22 (fls. 500)
- Total bloqueado 2026: R$ 83.752,42 (fls. 123) — **queda de −99,8%**

---

## Arquivos relacionados

- `pesquisas/sisbajud-dicionario-codigos.csv` — dicionário completo dos códigos
- `pesquisas/sisbajud-cruzamento-instituicoes-2023x2026.csv` — comparativo instituição por instituição (3 momentos: requisição 2023, bloqueio 2023, bloqueio 2026)
- `pesquisas/sisbajud-causas-divergencia.csv` — três causas técnicas detalhadas
- `pesquisas/sisbajud-validacao-correcoes.csv` — auditoria das correções da v1 → v2
- `pesquisas/sisbajud-planilha-explicativa.xlsx` — planilha consolidada (5 abas: Dicionário, Cruzamento, Causas, Validação, Síntese Executiva)

## Observação metodológica

Esta nota foi elaborada **exclusivamente a partir dos documentos juntados nesta sessão** (planilha Gorenstein, PDFs de bloqueio 2023 e 2026, parecer analítico v10). Valores e relações citados refletem o que consta dos autos validados; nenhum dado adicional foi assumido. Onde a fonte é silenciosa (ex.: extrato 12 meses), a recomendação é diligência futura, não conclusão de fato.
