"""Configuração central do pipeline cognitivo corporativo."""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


def load_json(filename: str) -> dict:
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


SISBAJUD_CODES = load_json("sisbajud_codes.json")
INSTITUTIONS_DATA = load_json("institutions.json")
ASSETS_DATA = load_json("assets.json")

RISK_THRESHOLDS = {
    "drain_ratio_critical": 0.90,
    "drain_ratio_high": 0.50,
    "non_response_days_critical": 5,
    "pl_variance_threshold_pct": 15.0,
    "min_asset_value_alert": 100_000.0,
}

LEGAL_FRAMEWORKS = {
    "art_171_CP": {
        "description": "Estelionato (art. 171 CP)",
        "penalty": "Reclusão de 1 a 5 anos e multa",
        "aggravated_penalty": "Reclusão de 4 a 8 anos e multa (§ 3º)",
    },
    "CPC_792": {
        "description": "Fraude à execução (art. 792 CPC)",
        "effect": "Ineficácia do ato em relação ao exequente",
    },
    "CC_50": {
        "description": "Desconsideração da personalidade jurídica (art. 50 CC)",
        "effect": "Extensão da responsabilidade aos sócios e administradores",
    },
    "Lei_9613_98": {
        "description": "Lavagem de dinheiro (Lei 9.613/98)",
        "penalty": "Reclusão de 3 a 10 anos e multa",
        "reporting_obligation": "COAF / Ministério Público Federal",
    },
}

REPORTING_TARGETS = {
    "CLO": "Chief Legal Officer – Núcleo de Governança",
    "IDPJ": "Núcleo de Investigação de Desconsideração da Personalidade Jurídica",
    "COAF": "Conselho de Controle de Atividades Financeiras",
    "MPF": "Ministério Público Federal",
}
