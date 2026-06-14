# Pipeline Cognitivo Corporativo
**Integração entre Tecnologia, Governança Jurídica e Investigação Patrimonial**

Sistema automatizado de investigação patrimonial capaz de detectar fraude, mapear ocultação, identificar ativos penhoráveis e produzir relatórios jurídicos de alto impacto.

---

## Arquitetura — 5 Módulos

```
BRIEFING → SYSTEM HEALTH CHECK → DEPENDENCY UPDATE → FLAKY TRACKER → PR REVIEW DIGEST
```

| Módulo | Função Técnica | Função Jurídica |
|---|---|---|
| **BRIEFING** | Agregação de dados (CVM, SISBAJUD, bancos) | Daily intelligence report, status SISBAJUD, alertas de bloqueio |
| **HEALTH CHECK** | APIs, integradores, Datadog | Divergência PL×IRPF, ausência de resposta, ocultação patrimonial |
| **DEPENDENCY UPDATE** | Atualização de bases CVM/IRPF/FATCA | Criação retroativa de classes, side-pockets, SPVs pós-litígio |
| **FLAKY TRACKER** | Inconsistências estatísticas, séries temporais | Iliquidez falsa, esvaziamento tático, padrão coordenado |
| **PR REVIEW DIGEST** | Consolidação de relatórios e pareceres | Enquadramento penal, mapa de ativos, minutas COAF/MPF |

---

## Uso

```bash
# Executa pipeline completo com saída no terminal
python main.py

# Gera relatório em arquivo (reports/)
python main.py --report

# Execução silenciosa (exit code 1 se houver alertas críticos)
python main.py --quiet

# Data específica
python main.py --date 2026-06-14 --report
```

---

## Estrutura

```
pesquisa-juridica-/
├── main.py                        # Ponto de entrada
├── pipeline/
│   ├── config.py                  # Configuração central
│   ├── models.py                  # Modelos de dados
│   ├── pipeline.py                # Orquestrador
│   ├── report_generator.py        # Gerador de relatórios
│   └── modules/
│       ├── briefing.py            # Módulo 1 — Briefing
│       ├── health_check.py        # Módulo 2 — Health Check
│       ├── dependency_update.py   # Módulo 3 — Dependency Update
│       ├── flaky_tracker.py       # Módulo 4 — Flaky Tracker
│       └── pr_review_digest.py    # Módulo 5 — PR Review Digest
├── data/
│   ├── assets.json                # Whole Money Trail
│   ├── institutions.json          # Instituições e ativos mapeados
│   └── sisbajud_codes.json        # Códigos e flags SISBAJUD
└── reports/                       # Relatórios gerados
```

---

## Enquadramento Jurídico

- **Art. 171 CP** — Estelionato
- **Art. 792 CPC** — Fraude à execução
- **Art. 50 CC** — Desconsideração da personalidade jurídica
- **Lei 9.613/98** — Lavagem de dinheiro (COAF / MPF)
