# PORTFÓLIO FINANCEIRO-CONTÁBIL — Caso de divórcio e partilha
## Mapeamento consolidado das pessoas (por papel processual) e entidades (por CNPJ) envolvidas direta ou indiretamente

> **Natureza:** parecer de perito contábil-forense (camada de consolidação). Organiza, em visão única, o universo patrimonial relevante à partilha, com atributos contábil-financeiros, grau probatório e vínculo de cada nó ao caso.
>
> **Sob o [MANIFESTO.md](../MANIFESTO.md):** pessoas físicas referidas **pelo papel processual** (Requerente, Requerido, terceiros por função); **CPF apenas do Requerido**, por ser dado público dos autos; **entidades por CNPJ**; **sem rótulo criminal categórico**; itens dependentes de checagem marcados **[CONFERIR]**. Terceiros não-partes **não** entram por dados pessoais — apenas por **função em ato societário público**, quando indispensável.
>
> **Processo principal:** 1006744-58.2023.8.26.0011 — 1ª Vara de Família e Sucessões de Pinheiros/SP. **Regime:** comunhão parcial (CC 1.658-1.660). **Constrição SISBAJUD:** desde 23/05/2023.
>
> ⚠️ **Discrepância a resolver:** material recente (roteiro HTML) refere os **autos 1050640-10.2025.8.26.0100** — verificar se é ação conexa autônoma ou erro de referência. **[CONFERIR]**

---

## 1. Mapa de camadas (visão contábil-forense)

A estrutura patrimonial relevante organiza-se em **cinco camadas funcionais**. A penhorabilidade e a comunicabilidade decrescem da Camada 3 (operacional, líquida) para a Camada 5 (offshore, opaca) — e é justamente esse gradiente que sustenta a tese de **iliquidez aparente**.

```
CAMADA 1 — PARTES (PF)
   Requerente (meeira) ──── vínculo conjugal ──── Requerido (CPF 136.447.108-64)
                                                        │ titularidade de cotas
                                                        ▼
CAMADA 2 — VEÍCULOS DE CONCENTRAÇÃO (FIPs)
   FIP Ajaccio (37.381.595/0001-82) · Volimo · Bonifácio · [XPA/Avila/Sharp — papel a confirmar]
                                                        │ 100% do ativo
                                                        ▼
CAMADA 3 — OPERACIONAL (geração de valor — líquido)
   E-Vino (17.392.519/0001-65) · Grand Cru · Agro Syrah/Vissimo · Vila Porto
                                                        │ fluxos de extração
                                                        ▼
CAMADA 4 — BLINDAGEM/PASSAGEM (PJ nacional)
   Ari Apoio Adm. (17.867.118/0001-14) · RT127 · SPE Abecker
                                                        │ saída
                                                        ▼
CAMADA 5 — OFFSHORE (opacidade)
   Anacapri · Brescia · Cetara · JP2R (Singapura) · Wine in Black (Berlim) · ACPE (Uruguai)

INFRAESTRUTURA FINANCEIRA (custódia/administração):
   Oslo Capital DTVM (ex-FRAM, 13.673.855/0001-25) · Vinci (gestora) · BTG (custodiante)
   Bancos com resposta SISBAJUD: Itaú · BTG · C6 · Nu · MercadoPago · [N26 SCD / BEXS — silêncio]
```

---

## 2. Inventário das pessoas físicas (por papel)

| Papel | Identificação permitida | Relevância contábil-patrimonial | Status Manifesto |
|---|---|---|---|
| **Requerente** | Meeira; parte; [condição relevante p/ prioridade — Lei 13.146/2015, off-repo] | Titular de 50% do patrimônio comum (CC 1.660) | Dados pessoais **fora** desta camada |
| **Requerido** | CPF 136.447.108-64 (público dos autos) | Titular formal das cotas do FIP Ajaccio e das participações operacionais; centro da apuração de iliquidez | CPF do Requerido = dado público da parte |
| **Cessionário de cotas** | Função pública: cessionário no Acordo de Cotistas [Ricardo F. de S. Costa, conforme ato societário — CONFERIR] | Cessão de ~4,42% das cotas (evento de liquidez transfronteiriço a apurar) | Apenas função em ato público; sem dados pessoais |
| **Co-administrador identificado** | Função: co-gestão/diretorias [CONFERIR no registro] | A confirmar nos autos antes de qualquer uso | Sem dados pessoais; só se confirmado em ato público |

> Detalhe em `pesquisas/portfolio-pessoas-papel-processual.csv`.

---

## 3. Inventário das pessoas jurídicas e fundos (por CNPJ)

Visão contábil resumida. Detalhamento completo (capital, PL, marcação, liquidez, fonte) em `pesquisas/portfolio-entidades-consolidado.csv`.

### 3.1. Camada 2 — Veículos de concentração (FIPs)

| Entidade | CNPJ | Atributo contábil-chave | Vínculo ao caso |
|---|---|---|---|
| FIP Ajaccio Multiestratégia | 37.381.595/0001-82 | PL ~R$ 1,53-1,57 bi; 100% em companhia fechada; caixa residual (~R$ 5.812,88) [CONFERIR] | **Nó central** — cotas sob constrição |
| Volimo FIP | 36.642.430/0001-54 | Mútuo conversível em ações E-Vino [CONFERIR] | Conversão em janela próxima ao litígio |
| Bonifácio FIP | 59.402.540/0001-44 | Constituído 11/02/2025 (litispendência) [CONFERIR] | Reorganização em curso de litígio |
| XPA Trafalgar / Avila / Sharp | [CONFERIR] | Papel: cotistas do Ajaccio **ou** veículos em que o Requerido é cotista? | **Define a NT Cotistas** |

### 3.2. Camada 3 — Operacional

| Entidade | CNPJ | Atributo contábil-chave | Vínculo ao caso |
|---|---|---|---|
| E-Vino Comércio de Vinhos S.A. | 17.392.519/0001-65 | Capital social ~R$ 537,9 mi; faturamento ~R$ 288 mi (2024) [CONFERIR] | Único ativo do Ajaccio; cisão 31/12/2021 |
| Grand Cru Importadora | [CONFERIR] | Adquirida pela E-Vino (2021) | Cluster operacional |
| Agro Syrah / Vissimo | [CONFERIR] | Holding operacional | E-mail corporativo em ato societário pós-"demissão" |
| Vila Porto Vinhos | [CONFERIR] | Contrato 01/07/2025 (R$ 50 mil/mês) | Possível violação de não-concorrência |

### 3.3. Camada 4 — Blindagem/passagem

| Entidade | CNPJ | Atributo contábil-chave | Vínculo ao caso |
|---|---|---|---|
| Ari Gorenstein Apoio Administrativo Ltda. | 17.867.118/0001-14 | Saldo médio reduzido; fluxo de passagem [CONFERIR extrato] | Possível confusão patrimonial (CC 50) |
| RT127 Empreendimentos | NIRE 35.238.272.663; CNPJ [CONFERIR] | Recebeu cisão R$ 57.180.967,46; distratada | Fraude contra credores (CC 158) |
| SPE Abecker | [CONFERIR] | Capital ~R$ 7,18 mi; juntada 31/03/2026 | Imobilização em véspera de audiência |

### 3.4. Camada 5 — Offshore

| Entidade | Jurisdição | Identificação | Vínculo ao caso |
|---|---|---|---|
| Anacapri | Delaware / BR | CNPJ 43.028.251/0001-97 [CONFERIR] | Cotista offshore (Acordo); lead UBO |
| Brescia | Delaware / BR | CNPJ 29.522.741/[CONFERIR] | Cotista offshore (Acordo) |
| Cetara | Delaware / BR | CNPJ 29.485.363/[CONFERIR] | Cotista offshore (Acordo) |
| JP2R PTE LTD | Singapura | UEN 201840728Z [CONFERIR] | Titularidade **contraditória** — a dirimir |
| Wine in Black GmbH | Alemanha | [HRB a CONFERIR] | Credora (€2,27 mi); destino da cisão |
| ACPE Advisors | Uruguai | [CONFERIR] | Cluster sul-americano |

### 3.5. Infraestrutura financeira (administração/custódia/bancos)

| Entidade | CNPJ | Papel | Ponto de atenção |
|---|---|---|---|
| Oslo Capital DTVM (ex-FRAM) | 13.673.855/0001-25 | Administradora do FIP | Iliquidez declarada sem prova; GIIN FATCA [CONFERIR] |
| Oslo Soberano FIF RF Simples | 62.194.627/0001-88 [CONFERIR] | Fundo da mesma administradora | Ilustra capacidade operacional (não prova falsidade) |
| Vinci Capital Gestora / Vinci Compass | 11.079.478/0001-75 [CONFERIR] | Gestora (desde 04/06/2024) | Conflito de interesse a apurar |
| BTG Pactual | [CONFERIR] | Custodiante | Retenção/desbloqueio a apurar |
| Itaú / C6 / Nu / MercadoPago | (autos) | Bancos com resposta SISBAJUD | Saldos confirmados em 2023 |
| N26 SCD / BEXS Câmbio | (autos) | Silêncio reiterado (código 98) | Possível embaraço — BACEN |

---

## 4. Quantificação preliminar da meação (visão contábil)

| Parcela | Base (R$) | Meação 50% (R$) | Status |
|---|---|---|---|
| Núcleo SISBAJUD localizado (mai/2023) | 84.856.714,65 | 42.428.357,32 | Bloqueio efetivado [CONFERIR conversão] |
| PL real do FIP Ajaccio (participação efetiva do Requerido) | a apurar sobre ~1,53-1,57 bi | **a apurar** | **Exposição potencial maior** |
| Non-compete | 749.183,38 | 374.591,69 | A integrar |
| Cisão E-Vino → RT127 | 57.180.967,46 | 28.590.483,73 | A reverter (CC 158) |
| Incontroverso (cumprimento conexo) | 66.443,47 [CONFERIR] | 33.221,74 | A levantar |

> **Observação contábil decisiva:** o valor já bloqueado (R$ 42,4 mi) tutela apenas o **núcleo declarado**. A diferença entre esse número e a **participação efetiva do Requerido no PL do Ajaccio** (a apurar) é o **gap patrimonial** que justifica as diligências de transparência.

---

## 5. Relatórios e notas técnicas que compõem o portfólio

| Documento | Caminho no repositório | Função no portfólio |
|---|---|---|
| Nota técnica SISBAJUD 2023×2026 (v2) | `notas/sisbajud-codigos-2023x2026-nota-tecnica.md` | Eixo bancário |
| Parecer omissão Ajaccio (KPMG) | `notas/parecer-ajaccio-omissao-bloqueio-cotas.md` | Eixo contábil-fiduciário |
| Roteiro pré-investigativo (falsa iliquidez) | `notas/roteiro-pre-investigativo-falsa-iliquidez-ajaccio.md` | Eixo justa causa |
| Dossiê integrado | `notas/dossie-integrado-ari-gorenstein-inteligencia-financeira.md` | Visão geral |
| Lead Anacapri | `notas/lead-anacapri-vinculo-offshore-investigacao.md` | Eixo offshore |
| Pacote de 7 notificações/representações | `notas/notificacoes/` | Eixo de provocação institucional |
| Minuta de representação ao MP | `notas/minuta-representacao-ministerio-publico.md` | Eixo criminal/lavagem |

---

## 6. Denúncias de boa-fé — princípio reitor

Todas as peças de provocação institucional deste portfólio observam o **princípio da boa-fé objetiva** e da **denúncia responsável**:

1. **Noticiam indícios — não afirmam crime.** Requerem **apuração** a quem detém os meios.
2. **Preservam a presunção de inocência** do Requerido e a **presunção de boa-fé** das instituições.
3. **Distinguem fato (E1), inferência (E2) e a-confirmar (E4).**
4. **Não atribuem rótulo criminal** sem prova produzida.
5. **Protegem o denunciante** contra reconvenção por litigância de má-fé ou denunciação caluniosa (CP 339) — a denúncia de boa-fé, ancorada em indício documental e dirigida ao órgão competente, **não** configura denunciação caluniosa.

> Quadro de canais e enquadramentos em `pesquisas/portfolio-fluxos-contabeis-apurar.csv`.

---

## 7. Diligências contábeis prioritárias (visão de perito)

1. **Apurar a participação efetiva do Requerido no PL do Ajaccio** — ofício à CVM (ficha de cotistas, datas, valor das cotas). Define o **gap patrimonial**.
2. **Reconstituir o fluxo E-Vino → Ari Apoio Adm. → PF** — extrato bancário; sustenta IDPJ (CC 50).
3. **Rastrear a cisão R$ 57.180.967,46 (E-Vino → RT127 → exterior)** — JUCESP + extratos.
4. **Confirmar a contabilização (ou não) da constrição** nos relatórios do FIP — perícia sobre os informes.
5. **Identificar o beneficiário final** das offshores Anacapri/Brescia/Cetara — UBO (IN RFB 2.119/2022).
6. **Dirimir a titularidade da JP2R** — ponto contraditório, não pode virar afirmação.
7. **Mapear marcação a valor justo** do ativo único (E-Vino) — perícia contábil; competência valorativa da CVM.

---

## 8. Observância metodológica

Portfólio consolidado **exclusivamente** a partir dos documentos do acervo desta sessão e de fontes oficiais públicas (CVM, JUCESP, RFB, autos). Pessoas físicas por papel; CPF apenas do Requerido (dado público da parte); entidades por CNPJ; terceiros não-partes sem dados pessoais. Itens **[CONFERIR]** dependem de checagem em fonte oficial antes de uso forense. Documento de apoio — **não protocolar** sem subscrição de advogado(a) e, no que couber, laudo de perito contábil habilitado (CRC).
