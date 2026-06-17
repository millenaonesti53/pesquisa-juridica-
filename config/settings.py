"""
Configuration settings for the Corporate Cognitive Pipeline.

This module centralises all tunable constants, API simulation parameters,
and threshold values used across the pipeline modules.
"""

from decimal import Decimal
from typing import Final

# ---------------------------------------------------------------------------
# Pipeline identity
# ---------------------------------------------------------------------------
PIPELINE_NAME: Final[str] = "Corporate Cognitive Pipeline — Pesquisa Jurídica"
PIPELINE_VERSION: Final[str] = "1.0.0"

# ---------------------------------------------------------------------------
# Monetary thresholds (BRL)
# ---------------------------------------------------------------------------

# Minimum absolute balance drop to trigger a tactical-emptying alert
TACTICAL_EMPTYING_THRESHOLD: Final[Decimal] = Decimal("50000.00")

# Proportional drop (0.0–1.0) that also triggers the alert
TACTICAL_EMPTYING_RATIO: Final[Decimal] = Decimal("0.90")

# Side-pocket suspicion: FIP with illiquid fraction above this ratio
SIDE_POCKET_ILLIQUID_RATIO: Final[Decimal] = Decimal("0.30")

# Statistical anomaly: z-score threshold for balance history
ANOMALY_Z_SCORE: Final[float] = 2.5

# ---------------------------------------------------------------------------
# SISBAJUD simulation
# ---------------------------------------------------------------------------
SISBAJUD_TIMEOUT_SECONDS: Final[int] = 30
SISBAJUD_MAX_RETRIES: Final[int] = 3

# ---------------------------------------------------------------------------
# Known litigation reference date (used to flag post-litigation asset creation)
# ---------------------------------------------------------------------------
LITIGATION_START_DATE: Final[str] = "2022-03-15"

# ---------------------------------------------------------------------------
# CVM / regulatory API simulation endpoints (not called — simulation only)
# ---------------------------------------------------------------------------
CVM_API_BASE: Final[str] = "https://dados.cvm.gov.br/api"
SISBAJUD_API_BASE: Final[str] = "https://sisbajud.cnj.jus.br/api"

# ---------------------------------------------------------------------------
# Output defaults
# ---------------------------------------------------------------------------
DEFAULT_OUTPUT_DIR: Final[str] = "output"
REPORT_DATE_FORMAT: Final[str] = "%Y-%m-%d"
REPORT_DATETIME_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S"

# ---------------------------------------------------------------------------
# Legal reference labels (used in alerts)
# ---------------------------------------------------------------------------
LEGAL_REFS = {
    "art_171_cp": "Art. 171 CP — Estelionato / Fraude",
    "art_792_cpc": "Art. 792 CPC — Fraude à Execução",
    "art_50_cc": "Art. 50 CC — Desconsideração da Personalidade Jurídica",
    "law_9613_98": "Lei 9.613/98 — Lavagem de Dinheiro",
    "fatca_crs": "FATCA/CRS — Reporte Internacional",
}
