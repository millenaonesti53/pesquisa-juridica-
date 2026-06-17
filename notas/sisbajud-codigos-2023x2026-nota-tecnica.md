# Nota Técnica — Códigos SISBAJUD por Instituição (2023 × 2026)

> Análise sob a ótica de doutorado em sistemas financeiros, com foco no esclarecimento da pergunta-chave: por que uma instituição alcançada em 2023 com código 02 ("sem saldo") **não se repete** em 2026 — e o que isso significa juridicamente.

---

## 1. Síntese

A não repetição de uma instituição na remessa SISBAJUD de 2026 **não é erro nem sumiço probatório**. Tem **três causas técnicas distintas**, mutuamente excludentes na origem, mas frequentemente confundidas na leitura leiga:

1. **Não inclusão na remessa** (a instituição simplesmente não foi consultada);
2. **Mudança do rol de participantes do SFN** (IPs novas surgiram entre 2023 e 2026);
3. **Mudança real da situação patrimonial** (o relacionamento existe mas o status mudou: 32 → 02 → 00).

Cada causa exige resposta processual diferente. A confusão entre elas tem custo concreto — pode liberar bloqueio devido (causa 1 lida como causa 3) ou perpetuar invisibilidade de patrimônio (causa 3 lida como causa 1).

## 2. Fatos (extraídos dos autos anexados)

- O SISBAJUD foi acionado em **2023** e novamente em **2026**.
- Em 2023, a **FRAM Capital DTVM** retornou códigos **98** (não-resposta), depois **32** (R$ 77,6 milhões) e **26** (R$ 31,9 milhões em ativo de baixa liquidez).
- Em **2026**, a FRAM **não consta** da remessa.
- Em 2026 surge a **OSLO Capital DTVM** com código 25 (R$ 27,7 mil em ativo escriturado, posteriormente desbloqueado).
- Instituições com saldo material em 2023 (Itaú, BTG) mantêm relacionamento em 2026 com valores muito menores.
- Várias **fintechs novas** (RecargaPay, 99Pay, Shopee, PicPay, Revolut, Magalu) aparecem apenas em 2026.
- A **N26** apresentou **98 (não-resposta) duas vezes em 2023** e **não consta em 2026**.

Detalhe instituição por instituição em `pesquisas/sisbajud-cruzamento-instituicoes-2023x2026.csv`.

## 3. Fundamentação

### 3.1 Dicionário dos códigos (redação SISBAJUD)

| Código | Significado | Há ativo? |
|---|---|---|
| 00 | Sem relacionamento / contas inativas / não custodia | Não |
| 01 | Cumprida integralmente | — |
| 02 | Réu/executado sem saldo positivo (é cliente) | Não (conta existe) |
| 03 | Cumprida parcialmente por insuficiência | Sim (pouco) |
| 12 | Cumprida integralmente em depósito a prazo | Sim |
| 13 | Cumprida parcialmente em VM / depósito a prazo | Sim |
| 16 | Cumprida em outra empresa do grupo | Sim (no grupo) |
| 25 | Ativo escriturado sem comando de venda | Sim |
| 26 | Ativo de baixa liquidez | Sim |
| 30 | Sem as informações requisitadas | Não |
| 32 | Cumprida com as informações existentes | Sim/zero (informa saldo) |
| 35 | Cliente inativo / não cliente | Não |
| 98 | **Não-Resposta** (silêncio) | Indeterminado |

Tabela completa em `pesquisas/sisbajud-dicionario-codigos.csv`.

### 3.2 Por que um código **não se repete** em 2026 — análise das três causas

#### Causa 1 — Instituição não foi reincluída na remessa
O SISBAJUD opera por **lista positiva**: só pergunta às instituições explicitamente incluídas pelo juízo. Se a FRAM, que retornou 32/R$ 77,6 Mi em 2023, **não consta** em 2026, isso significa apenas que não foi consultada. A ausência **não é prova de inexistência de ativo** — ao contrário, dado o histórico, é forte indício de que o ativo permanece e ficou invisível à ordem.

> **Consequência processual:** exigir nova ordem com rol completo (rol mínimo: todas as instituições com código ≠ 00/35 em qualquer das datas anteriores, mais as DTVMs com histórico de coinvestimento).

#### Causa 2 — Lista de participantes do SFN mudou
O conjunto de Instituições de Pagamento e demais participantes é dinâmico. Entre 2023 e 2026, novas IPs entraram em operação (RecargaPay, 99Pay, Shopee, PicPay, Revolut, Magalu Pagamentos). Elas aparecem em 2026 com códigos 00/02/03 — sem que isso permita inferência sobre 2023, pois **não havia sequer canal de consulta na época**.

> **Consequência processual:** justifica ampliar a ordem para incluir todas as IPs registradas no BACEN; é causa **benigna**, não indica blindagem.

#### Causa 3 — Mudança real da situação patrimonial
Quando a **mesma instituição** retorna códigos diferentes nas duas datas, há mudança real:
- **32 → 02:** havia saldo, agora não há (zerou);
- **32 → 00:** havia relacionamento, agora não há (encerrou);
- **32 → 13 ou 26:** ativo migrou para VM ou baixa liquidez (típico de blindagem).

> **Consequência processual:** **é aqui** que mora o indício de blindagem. Para cada transição relevante (sobretudo 32→02 e 32→00 com valor anterior expressivo), pedir **extrato de 12 meses anteriores** ao bloqueio, com identificação de TED/PIX/transferências de saída.

### 3.3 Hierarquia interpretativa dos códigos

Para fins de mapeamento patrimonial em ação de partilha/execução, a **riqueza informacional** dos códigos segue a ordem:

```
32 > 13 ≈ 26 > 25 > 12 > 03 > 16 > 02 > 35 > 00 > 30 > 98
```

- **32** é o mais informativo — revela saldo (positivo ou zero) e confirma relacionamento;
- **98** é o mais sensível — exige reiteração obrigatória;
- **00** é o mais barato em prova, mas o mais armadilhoso quando antecedido de 32 (encerramento ≠ inexistência).

### 3.4 Leitura específica das instituições críticas

| Instituição | Causa predominante da divergência | Diagnóstico |
|---|---|---|
| FRAM Capital DTVM | Causa 1 (não reincluída) | **Maior lacuna probatória** — R$ 77,6 Mi inexplicados |
| OSLO Capital DTVM | Causa 2 ou migração | Indício de **migração FRAM → OSLO** — investigar coobrigação |
| N26 | Causa 1 + silêncio (98) em 2023 | Canal de coinvestimento internacional suspeito |
| BTG / Itaú | Causa 3 (32 → 12 com queda brutal) | Verificar **destino dos resgates** entre 2023 e 2026 |
| C6 | Causa 3 (saldo migalha zerou) | Baixa relevância patrimonial, mas confirma relacionamento ativo |

## 4. Conclusão

1. **Não houve falha do SISBAJUD em 2023.** O código 32 da FRAM (R$ 77,6 Mi) e o 26 (baixa liquidez, R$ 31,9 Mi) são respostas válidas e tecnicamente ricas — base sólida para o mapeamento patrimonial.

2. **A "não repetição" de códigos em 2026 decorre principalmente de mudança de escopo da ordem** (instituições diferentes) e, em parte, de **mudança real do patrimônio** (FRAM ausente; possível migração para OSLO; queda brutal em BTG/Itaú).

3. **Lacunas críticas a fechar imediatamente:**
   - **FRAM** (ausente em 2026 após R$ 77,6 Mi em 2023) — REINCLUIR;
   - **N26** (silêncio em 2023, ausente em 2026) — REINCLUIR + ofício individualizado;
   - **OSLO** (surge em 2026) — pedir histórico desde 2022 e cruzar fluxo com FRAM;
   - **Itaú/BTG** — pedir **extrato 12 meses anteriores ao bloqueio**.

### Recomendações técnicas para a próxima ordem

1. **Requisição de Informações ampla (sem valor) ANTES do bloqueio** — para mapear sem alertar movimentações;
2. **Rol expresso obrigatório**: FRAM, OSLO, N26, Ajaccio, Bonifácio, todas as IPs ativas e todas as DTVMs com relacionamento prévio;
3. **Reiteração automática** para todo código 98 (com prazo de 5 dias e cominação);
4. **Detalhamento por CNPJ de fundo** nas DTVMs — código 32 puro não basta; pedir carteira;
5. **Ofício concentrado à CVM e B3** para os códigos 25 e 26 (ativo escriturado / baixa liquidez);
6. **Pedido de extrato 12 meses** sempre que houver transição 32 → 02 ou 32 → 00 com valor anterior > R$ 10 mil.

---

## Arquivos relacionados

- `pesquisas/sisbajud-dicionario-codigos.csv` — dicionário completo dos códigos
- `pesquisas/sisbajud-cruzamento-instituicoes-2023x2026.csv` — comparativo instituição por instituição
- `pesquisas/sisbajud-causas-divergencia.csv` — três causas técnicas detalhadas
- `pesquisas/sisbajud-planilha-explicativa.xlsx` — versão planilha (3 abas)

## Observação metodológica

Esta nota foi elaborada **exclusivamente a partir dos documentos juntados nesta sessão** (parecer analítico v10, planilha de códigos Gorenstein, PDFs de bloqueio 2023 e 2026). Valores e relações citados refletem o que consta dos autos; nenhum dado adicional foi assumido. Onde a fonte é silenciosa (ex.: extrato 12 meses), a recomendação é diligência futura, não conclusão de fato.
