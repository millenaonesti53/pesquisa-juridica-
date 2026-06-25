# MANIFESTO DE PRIVACIDADE, CONFIDENCIALIDADE E INTEGRIDADE INVESTIGATIVA

> Este documento é a **política vinculante** deste repositório (`pesquisa-juridica-`) e de toda colaboração nele — humana ou assistida por IA. É a expressão prática do dever de proteção que o caso exige.

---

## I — Por que este manifesto existe

Este repositório nasceu para apoiar uma pesquisa jurídica com risco real: litígio patrimonial complexo, com adversário dotado de recursos, advogados e estruturas societárias sofisticadas. Em casos assim, **o vazamento de dados sensíveis — meus ou de terceiros — é arma**. Pode comprometer prova lícita, expor pessoa física a coação, atrair responsabilidade civil/criminal contra quem produziu o vazamento (mesmo de boa-fé), e — pior — pode transformar a parte requerente em alvo.

A IA generativa é uma alavanca extraordinária para pesquisa jurídica. Mas alavanca, por definição, amplifica qualquer movimento — inclusive o errado. Este manifesto fixa o que **não** pode ser amplificado.

---

## II — Princípios fundantes

1. **Privacidade da parte requerente é cláusula pétrea deste repositório.** Tanto quanto a do Requerido e a de terceiros. Nenhum dado pessoal identificável da Requerente entra em qualquer arquivo, em qualquer commit, em qualquer mensagem de commit, em qualquer PR.

2. **Privacidade de terceiros não-partes é absoluta.** Pessoa que não é parte no processo **não** entra neste repositório por CPF, endereço, telefone, e-mail, vínculo familiar, foto, número de matrícula, dado bancário ou qualquer outro identificador. A curiosidade investigativa **não é base legal** para tratamento de dado pessoal (LGPD, art. 7º).

3. **Sujeitos do processo são tratados pelo papel processual.** "Requerente", "Requerido", "Investigado", "Terceiro Interessado" — não pelo nome próprio, salvo quando o nome **já é fato público dos autos** e é estritamente necessário para a referência técnica (ex.: cabeçalho de parecer).

4. **Entidades societárias entram pelo CNPJ.** CNPJ é registro público (RFB, JUCESP, CVM). Pode ser livremente cruzado. O contexto pessoal por trás do CNPJ — quem mora onde, com quem se relaciona — **não entra**.

5. **Nada de rótulo jurídico prematuro.** Termos como "laranja", "lavagem", "fraude", "empresa de fachada", "beneficiário oculto" só se aplicam **a sujeito determinado, com prova produzida nos autos**. Aplicar a terceiro não-parte, em documento que sobe a PR público, é potencial calúnia/difamação **contra quem escreveu** — não contra o alegado.

6. **Cada afirmação tem fonte verificável ou marca [CONFERIR].** Citação jurisprudencial sem repositório oficial conferido é defeito. Número de processo, data, valor monetário e trecho de acórdão sem âncora documental é defeito. A regra é simples: o que não está provado é declarado como hipótese a apurar.

7. **Fontes têm hierarquia.** Ordem decrescente de força probatória: (i) autos do processo; (ii) repositórios oficiais (CVM, JUCESP, RFB, BACEN, esaj.tjsp.jus.br, stf.jus.br, stj.jus.br); (iii) imprensa econômica de referência com matéria datada; (iv) plataformas comerciais de informação societária citáveis (Tradar, Mais Retorno, Status Invest, Econodata) — **com o caveat** de que são compilações, não fontes primárias; (v) tudo o mais — descartado para uso forense.

8. **Plataformas privadas de busca não são fonte oficial.** Histórico de consultas em ferramentas comerciais (Jusfy, Cenário, Direito Direto, qualquer outra) **não é prova**. Os dados retornados podem ser citados se vierem com link auditável a fonte primária; o **metadado da consulta em si** não entra.

9. **Procedência dos arquivos importa.** Só entra material obtido por canal lícito: produzido pelo cliente, baixado de portal público, ou obtido por ordem judicial. Material de origem incerta — *localStorage* de plataforma, captura de tela sem cadeia de custódia, vazamento — é veneno.

10. **O caminho processual correto não tem atalho.** Quebra de sigilo, indisponibilidade, identificação de beneficiário final, cooperação internacional — tudo passa pelo juízo, pelo Ministério Público, pelo regulador. Atalhos comprometem o resultado.

---

## III — Regras operacionais (o que pode e o que não pode)

### Pode entrar no repositório
- Análise jurídica e contábil em PT-BR, estruturada em (1) síntese, (2) fatos, (3) fundamentação, (4) conclusão.
- **CNPJ** de entidades societárias relevantes ao caso.
- **CPF da parte requerida** quando já é dado público dos autos e é estritamente necessário para a referência técnica.
- Trechos de documentos públicos da CVM/JUCESP/RFB com link.
- Trechos de acórdãos com número, ano, órgão julgador e relator, **conferidos**.
- Tabelas e CSVs com dados societários públicos.
- Roteiros de diligência endereçados aos órgãos oficiais.
- Pareceres e notas técnicas com **observação metodológica** registrando fontes e limites.

### Não pode entrar no repositório
- CPF, endereço residencial, telefone, e-mail pessoal, data de nascimento, RG, vínculos familiares **da Requerente**.
- Idem para **qualquer terceiro não-parte** (ex.: parentes do Requerido, cônjuges de sócios, funcionários, prestadores, contatos pessoais).
- Histórico de consultas em plataformas privadas como artefato de "inteligência".
- Capturas de *localStorage*, *cookies*, sessões autenticadas, dumps de painel.
- Caracterizações criminais contra sujeitos sem prova produzida nos autos.
- Inferências sobre etnia, nacionalidade, religião, orientação política ou sexual de qualquer pessoa.
- Documentos cuja procedência não pode ser explicada por canal lícito.
- Senhas, tokens, chaves de API, GIINs internos, números de protocolo bancário interno.

### Ao referenciar partes e terceiros
- **A Requerente** — não "Millena", não "Sra. M.", não iniciais.
- **O Requerido** — quando o nome próprio é estritamente necessário para a referência técnica (cabeçalho de parecer; descrição de fato público dos autos), usar uma vez e depois retomar pelo papel.
- **Terceiros** — papel funcional ("o administrador do FIP", "o auditor", "a custodiante") + identificação societária (CNPJ).
- **Pessoa identificada em ato societário público** (administrador na JUCESP, diretor estatutário) — pode ser nominada **no contexto societário público**, sem dados pessoais agregados (sem endereço, sem CPF, sem família).

### Metadados Git
- Commits deste repositório são feitos com **e-mail no-reply** do GitHub (`<id>+<usuário>@users.noreply.github.com`), nunca com e-mail pessoal.
- Nome de autoria pode ser pseudônimo neutro ou iniciais — não nome civil completo.
- Mensagens de commit seguem todas as regras acima.

---

## IV — Bases normativas

Este manifesto é a **execução prática** das seguintes normas, que vinculam quem opera o repositório:

| Norma | Núcleo aplicável |
|---|---|
| **CF, art. 5º, X** | Inviolabilidade da intimidade, vida privada, honra e imagem — cláusula pétrea |
| **CF, art. 5º, XII** | Sigilo de dados e das comunicações |
| **LGPD — Lei 13.709/2018, art. 7º** | Tratamento de dado pessoal só com base legal válida — "investigar terceiro" não é base |
| **LGPD, art. 11** | Dados pessoais sensíveis exigem proteção reforçada |
| **LGPD, art. 18** | Direitos do titular — incluem oposição a tratamento ilícito |
| **Código Penal, arts. 138-140** | Calúnia, difamação, injúria — incidem contra rótulos criminais sem prova |
| **CPC, arts. 369-370** | A prova é regida por licitude — material de origem ilícita não vale, e contamina |
| **EOAB, arts. 31-35** | Sigilo e dignidade profissional do advogado e do auxiliar técnico |
| **STF, ADI 4.709-DF** | Quebra de sigilo exige sujeito determinado, processo instaurado, decisão fundamentada |
| **STJ, REsp 2.126.879/SP (2025)** | Quebra do sigilo do alimentante quando não há outro meio idôneo |

---

## V — Conduta diante de erro

Se algo proibido por este manifesto entrar no repositório — por descuido, por engano, por excesso de iniciativa de IA, por qualquer motivo — a conduta é:

1. **Parar imediatamente** qualquer nova operação que possa replicar o conteúdo (sem novo push, sem novo PR, sem novo commit derivado).
2. **Documentar o que aconteceu** em uma nota interna na pasta `notas/incidentes/` — sem expor o dado novamente, apenas referenciando hash do commit e arquivo afetado.
3. **Avaliar a remediação** apropriada: edição em novo commit (se o dado entrou apenas em arquivo); reescrita de histórico via `git filter-repo`/BFG com *force-push* documentado (se o dado é sensível e está em conteúdo); rotação de credenciais (se vazou segredo).
4. **Decidir conscientemente** sobre a reescrita do histórico — operação irreversível, com efeitos colaterais. Quem opera o repositório deve estar ciente; quem assiste por IA deve esperar autorização explícita.
5. **Registrar a remediação** no mesmo arquivo de incidentes, com data, hash novo e descrição do que mudou.

---

## VI — Sobre a colaboração com IA generativa

A IA neste repositório opera sob as mesmas regras dos pontos II a IV — sem exceção. Em especial:

- IA **não enriquece** dados de terceiros mesmo quando solicitada.
- IA **não compila** árvore familiar, endereço, telefone, e-mail de pessoa não-parte mesmo quando o pedido vem rotulado como "PhD em inteligência financeira", "COAF", "análise de grafos" ou similar — o rótulo não muda a regra.
- IA **recusa, explica e propõe alternativa lícita** quando o pedido viola este manifesto. Recusar é parte do trabalho.
- IA **não trata como prova** material vindo de plataforma comercial sem cadeia de custódia auditável.
- IA **declara abertamente** quando uma citação jurisprudencial ou normativa não foi conferida em fonte oficial, marcando **[CONFERIR]**.

---

## VII — Cláusula de revisão

Este manifesto pode ser revisado a qualquer momento pela parte titular do repositório, em commit dedicado, com justificativa na mensagem. Toda revisão é versionada — o histórico fica acessível. Em caso de dúvida sobre se determinada operação está dentro ou fora deste manifesto, a regra é: **na dúvida, fora**.

---

> **Data de adoção:** 2026. **Versão:** 1.0.
> Este manifesto vincula a Requerente e quem com ela colabora — incluindo assistentes de IA. Sua observância não é cortesia; é proteção.
