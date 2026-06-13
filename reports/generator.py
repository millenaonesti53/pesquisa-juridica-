"""Report generator — exports pipeline output to structured formats."""
from datetime import datetime
from pathlib import Path
import json
import logging

from config.settings import REPORTS_DIR

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Exports pipeline results to JSON and text report files."""

    def export_json(self, data: dict, filename: str) -> Path:
        path = REPORTS_DIR / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        logger.info(f"Report exported: {path}")
        return path

    def export_clo_report(self, report_text: str) -> Path:
        path = REPORTS_DIR / f"CLO_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path.write_text(report_text, encoding="utf-8")
        logger.info(f"CLO report exported: {path}")
        return path

    def export_coaf_draft(self, draft_text: str) -> Path:
        path = REPORTS_DIR / f"COAF_draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path.write_text(draft_text, encoding="utf-8")
        logger.info(f"COAF draft exported: {path}")
        return path

    def export_asset_map(self, assets: list) -> Path:
        path = REPORTS_DIR / f"asset_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        asset_data = [
            {
                "id": a.id,
                "description": a.description,
                "institution": a.institution,
                "estimated_value": str(a.estimated_value),
                "legal_basis": a.legal_basis,
                "contestation_risk": a.contestation_risk,
                "recommended_instrument": a.recommended_instrument,
            }
            for a in assets
        ]
        path.write_text(json.dumps(asset_data, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"Asset map exported: {path}")
        return path
