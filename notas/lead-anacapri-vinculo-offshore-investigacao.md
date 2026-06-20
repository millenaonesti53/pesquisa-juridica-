# Lead investigativo — Anacapri Investments e o vínculo com a camada offshore Gorenstein

> **Escopo restrito:** este documento trata exclusivamente de **entidades societárias** (CNPJ) com registro público em CVM, RFB e fontes equivalentes. **Não inclui dados pessoais de terceiros** (CPF, endereço, telefone, vínculos familiares) — em observância (i) ao art. 5º, X, da CF, (ii) à LGPD (Lei 13.709/2018) e (iii) ao próprio CLAUDE.md deste repositório.
>
> Pessoas físicas só aparecem quando **já são partes do processo** ou figuram em atos societários públicos verificáveis (administrador registrado na CVM/JUCESP).

---

## 1. Por que este lead importa

O dossiê integrado anterior (`notas/dossie-integrado-ari-gorenstein-inteligencia-financeira.md`, Camada 5) já indicava entre os veículos *offshore* da arquitetura Gorenstein:

> "**Brescia · Cetara · Anacapri · Raffaello** (Delaware LLCs)"

Em material externo apresentado agora, surge um **CNPJ brasileiro** com nome compatível:

> **"Anacapri Investments LLC"** — CNPJ **43.028.251/0001-97** — adm. **J.P. Morgan S/A DTVM** — situação cadastral ATIVA — início 06/08/2021 — domicílio "exterior" (campo EX = 1) — CNAE 6630-4/00 (administração de fundos por contrato ou comissão).

A hipótese a ser **testada com fonte oficial** é: *o CNPJ 43.028.251/0001-97 é o registro fiscal brasileiro da mesma "Anacapri" antes mencionada como Delaware LLC?*

Se for, abre-se um eixo investigativo **legítimo e novo**: a entidade está formalmente conectada ao sistema fiscal brasileiro (CNPJ ativo) e tem **administrador conhecido (J.P. Morgan DTVM)**, o que **torna a quebra de sigilo viável pelos canais regulatórios** (não precisa de cooperação internacional para o primeiro round).

## 2. O que verificar (fontes oficiais)

### 2.1. CVM — sistema de fundos e participantes do mercado
- **Portal CVM:** https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx
- **Dados Abertos CVM:** https://dados.cvm.gov.br/
- **O que apurar:**
  - Há fundo, classe ou subclasse vinculado ao CNPJ 43.028.251/0001-97?
  - Em qual qualidade J.P. Morgan S/A DTVM atua (administrador, custodiante, escriturador)?
  - Qual o gestor (CNPJ separado), o regulamento e a data do registro inicial?
  - Os Informes Quadrimestrais (FIPs/Fundos) trazem composição de cotistas? E há alguma referência a cotistas-PF residentes no Brasil?

### 2.2. Receita Federal — CNPJ
- **Consulta:** https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao.asp
- **O que apurar:** confirmação da situação ativa, CNAE, endereço, capital social, QSA (quadro de sócios e administradores), data da última atualização.

### 2.3. BACEN — IF.data e GIIN/FATCA
- **IF.data:** https://www3.bcb.gov.br/ifdata/
- **O que apurar:** autorização e GIIN do **J.P. Morgan S/A DTVM** (já temos o GIIN da OSLO Capital DTVM = `0W2JW5.99999.SL.076`; comparar e procurar elo de custódia/repasse via SWIFT).

### 2.4. JUCESP — atos societários (se houver filial/representação)
- **Portal:** https://www.jucesponline.sp.gov.br/
- **O que apurar:** existência de representação brasileira, atos de constituição/alteração, eventual gerente delegado.

### 2.5. Delaware Division of Corporations (fonte primária da LLC, se confirmada)
- **General Information Name Search:** https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx
- **O que apurar:** estado da formação ("formation"), agente de registro, data de incorporação. Delaware não publica beneficial owner (sob FinCEN BOI Report a regra mudou em 2024-2025 — verificar status atual no portal FinCEN https://www.fincen.gov/boi).

## 3. Como esse lead se encaixa no caso já documentado

| Eixo já documentado | Conexão proposta com este lead |
|---|---|
| **Camada 5 offshore** (Brescia/Cetara/Anacapri/Raffaello em Delaware) | Confirmar se o CNPJ 43.028.251/0001-97 é o registro fiscal brasileiro da mesma Anacapri |
| **Custodiantes/administradores** já sob suspeita (OSLO ex-FRAM; BTG) | Acrescenta J.P. Morgan S/A DTVM como possível elo adicional — apenas se a vinculação for confirmada |
| **DCBE** (Lei 14.286/21) | Se confirmada vinculação a Ari Gorenstein (CPF já público nos autos: 136.447.108-64), reforça-se o pedido de DCBE — agora com **CNPJ brasileiro identificado** |
| **Justa causa STF/STJ** (ADI 4.709-DF; REsp 2.126.879/SP) | A existência de CNPJ ativo no Brasil reduz o limiar para a cooperação investigativa interna — não exige MLAT para o primeiro round |

## 4. Caminho processual correto (NÃO contornar)

A apuração deste lead deve seguir **estritamente** o caminho que o STF e o STJ exigem:

1. **Petição ao juízo da partilha** (1ª Vara de Família e Sucessões de Pinheiros — autos 1006744-58.2023.8.26.0011) com:
   - Indicação do CNPJ 43.028.251/0001-97 como **lead** (não como fato);
   - Pedido de **ofício à CVM** requerendo: registro do fundo (se houver); QSA; identificação de cotistas-PF residentes no Brasil; cópia do regulamento.
   - Pedido de **ofício ao BACEN/RFB** sobre o GIIN do J.P. Morgan DTVM e eventuais reportes FATCA atrelados ao CPF 136.447.108-64.
2. **Em paralelo**, **representação à CVM** (Lei 6.385/76 art. 9º, V) **somente se** a vinculação for confirmada via item 1 — para apurar eventual omissão regulatória.
3. **Cooperação internacional (MLAT BR-EUA)** com Delaware reservada para o **segundo round**, apenas após a confirmação interna.

> Nada disso depende de dados pessoais de terceiros não-partes. O CNPJ é registro público; a quebra de sigilo é determinada por juiz; o resultado entra nos autos.

## 5. O que NÃO entra neste lead nem em qualquer commit deste repositório

- CPF, endereço residencial, telefone, e-mail, idade, sexo, vínculos familiares de **qualquer pessoa física que não seja parte** no processo.
- Histórico de buscas/consultas em plataformas privadas (Jusfy ou outras) — **não é fonte probatória oficial** e seu uso como "metadado de inteligência" levanta riscos legais (LGPD; eventual prova ilícita).
- Rótulos jurídicos prematuros ("laranja", "lavagem", "empresa de fachada") contra entidades **sem prova produzida** — gera responsabilidade civil e potencialmente criminal por calúnia/difamação contra o operador do dossiê.
- Inferências de etnia, nacionalidade ou religião a partir de sobrenomes — analiticamente inválido e juridicamente perigoso.
- Caracterizações negativas de SCP, EI ou capital social baixo como "indícios de crime" — são formas societárias **lícitas** previstas no Código Civil (arts. 991-996 e 968 a 980-A) e na Lei Complementar 123/2006.

## 6. Diligência mínima por entidade (apenas via CNPJ)

| Entidade (CNPJ) | Ação | Fonte oficial | Resultado esperado |
|---|---|---|---|
| 43.028.251/0001-97 (Anacapri Investments LLC — adm. J.P. Morgan DTVM) | Confirmar existência, QSA, regulamento, vinculação com cotistas Brasil | CVM / RFB / BACEN | Confirmação OU descarte do lead |
| 17.392.519/0001-65 (E-Vino S.A.) | Ato societário e composição (já documentado no dossiê) | JUCESP | Atualização do quadro |
| 17.867.118/0001-14 (MEI Apoio Adm.) | Situação cadastral, atividade, regime tributário | RFB | Atualização |

Esta tabela é deliberadamente curta. Cada nova entidade só deve ser adicionada **após** vinculação direta a Ari Gorenstein ou ao patrimônio em partilha, com fonte oficial citada.

---

## 7. Observância

- **CLAUDE.md:** documentos sensíveis (CPF, dados patrimoniais) **não publicados em PRs/commits**.
- **LGPD (Lei 13.709/2018):** tratamento de dado pessoal de terceiro exige base legal válida (art. 7º); a curiosidade investigativa **não** é base legal.
- **CF art. 5º, X:** privacidade de não-partes é cláusula pétrea.
- **STF / STJ:** os precedentes verificados (ADI 4.709-DF; REsp 2.126.879/SP; HC 750.740/SP) só blindam a quebra **se** ela for pedida ao juízo, **fundamentada** em indícios concretos e relativa ao **sujeito determinado** do processo — Ari Gorenstein.

Este documento, portanto, registra o **lead** (Anacapri-CNPJ-CVM) com o caminho oficial de verificação — e deixa fora tudo o que poderia comprometer a parte requerente.
