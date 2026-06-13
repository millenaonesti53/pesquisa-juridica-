"""Pipeline configuration and constants."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# SISBAJUD response codes
SISBAJUD_CODE_NO_RESPONSE = 98
SISBAJUD_CODE_NO_BALANCE = 13
SISBAJUD_CODE_BALANCE_FOUND = 1
SISBAJUD_CODE_BLOCKED = 2

# Risk thresholds
ABRUPT_VARIATION_THRESHOLD = 0.80  # 80% drop flags as suspicious
CRITICAL_BALANCE_FLOOR = 1000.0     # below R$1k after high balance = suspicious

# Legal framework references
LEGAL_REFS = {
    "estelionato": "Art. 171 CP",
    "fraude_execucao": "CPC Art. 792",
    "desconsideracao_personalidade": "CC Art. 50",
    "lavagem_dinheiro": "Lei 9.613/98",
    "impenhorabilidade_fip": "Lei 6.404/76 + CPC 833",
}

# Known institutions under monitoring
MONITORED_INSTITUTIONS = [
    "FRAM",
    "OSLO",
    "BTG",
    "ITAU",
    "BONIFACIO_FIP",
    "AJACCIO_FIP",
]

REPORTS_DIR = BASE_DIR / "reports" / "output"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
