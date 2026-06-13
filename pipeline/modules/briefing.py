"""
Module 1: BRIEFING
Aggregates daily intelligence from all sources and generates
the morning contextual report for the CLO and Governance Nucleus.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional
import logging

from models.assets import Asset, AssetType, RiskLevel
from models.alerts import Alert, AlertType, AlertSeverity
from config.settings import LEGAL_REFS

logger = logging.getLogger(__name__)


# Known asset registry (from investigation record)
KNOWN_ASSETS: list[Asset] = [
    Asset(
        id="FRAM_XIV_FIP",
        institution="FRAM",
        asset_type=AssetType.FIP,
        description="FRAM XIV FIP — Fundo de Investimento em Participações",
        balance=Decimal("3877255.47"),
        reference_date=datetime(2025, 3, 31),
        sisbajud_code=98,
        risk_level=RiskLevel.CRITICO,
        notes="Não respondeu SISBAJUD. PL divergente vs IRPF.",
        is_penherable=True,
    ),
    Asset(
        id="LIG_ITAU",
        institution="ITAU",
        asset_type=AssetType.LIG,
        description="LIG Itaú — Letra Imobiliária Garantida",
        balance=Decimal("1250000.00"),
        reference_date=datetime(2025, 3, 31),
        sisbajud_code=13,
        risk_level=RiskLevel.ALTO,
        notes="Respondeu código 13 (sem saldo). LIG alega impenhorabilidade.",
        is_penherable=False,
        legal_basis_impenhorability="Alegação: LIG coberta por garantia imobiliária. Contestável via CPC 835.",
    ),
    Asset(
        id="CDB_BTG",
        institution="BTG",
        asset_type=AssetType.CDB,
        description="CDB BTG Pactual",
        balance=Decimal("0.00"),
        reference_date=datetime(2025, 6, 1),
        previous_balance=Decimal("650758.60"),
        sisbajud_code=13,
        risk_level=RiskLevel.CRITICO,
        notes="Saldo zerado. Esvaziamento tático detectado. Saldo anterior: R$650.758,60.",
        is_penherable=True,
    ),
    Asset(
        id="ITAU_CC",
        institution="ITAU",
        asset_type=AssetType.CONTA_CORRENTE,
        description="Conta Corrente Itaú",
        balance=Decimal("5491.00"),
        reference_date=datetime(2025, 6, 1),
        previous_balance=Decimal("469575.00"),
        sisbajud_code=1,
        risk_level=RiskLevel.CRITICO,
        notes="Variação: R$469.575 → R$5.491 (-98.8%). Esvaziamento tático confirmado.",
        is_penherable=True,
    ),
]

INSTITUTION_STATUS = {
    "FRAM": {"sisbajud_code": 98, "last_query": "2025-05-20", "response": "NÃO RESPONDEU"},
    "OSLO": {"sisbajud_code": 98, "last_query": "2025-05-20", "response": "NÃO RESPONDEU"},
    "BTG": {"sisbajud_code": 13, "last_query": "2025-05-20", "response": "Saldo zero c/ movimentação prévia"},
    "ITAU": {"sisbajud_code": 1, "last_query": "2025-05-20", "response": "Saldo residual após esvaziamento"},
}


@dataclass
class BriefingReport:
    generated_at: datetime
    reference_date: date
    assets: list[Asset]
    institution_status: dict
    critical_alerts: list[Alert] = field(default_factory=list)
    total_identified: Decimal = Decimal("0")
    total_at_risk: Decimal = Decimal("0")
    whole_money_trail_summary: str = ""


class BriefingModule:
    """
    Daily intelligence aggregator.
    Loads the Whole Money Trail, updates institution status,
    and generates alerts for CLO and Governance Nucleus.
    """

    def run(self, reference_date: Optional[date] = None) -> BriefingReport:
        if reference_date is None:
            reference_date = date.today() - timedelta(days=1)

        logger.info(f"[BRIEFING] Starting daily briefing for {reference_date}")

        assets = self._load_asset_registry()
        institution_status = self._update_institution_status()
        alerts = self._generate_alerts(assets)
        total_identified = sum(a.balance for a in assets if a.balance > 0)
        total_at_risk = sum(
            a.balance for a in assets if a.risk_level in (RiskLevel.CRITICO, RiskLevel.ALTO)
        )

        report = BriefingReport(
            generated_at=datetime.now(),
            reference_date=reference_date,
            assets=assets,
            institution_status=institution_status,
            critical_alerts=alerts,
            total_identified=total_identified,
            total_at_risk=total_at_risk,
            whole_money_trail_summary=self._build_money_trail_summary(assets),
        )

        self._log_report(report)
        return report

    def _load_asset_registry(self) -> list[Asset]:
        logger.info("[BRIEFING] Loading asset registry")
        return KNOWN_ASSETS

    def _update_institution_status(self) -> dict:
        logger.info("[BRIEFING] Updating institution status")
        updated = {}
        for inst, data in INSTITUTION_STATUS.items():
            updated[inst] = {
                **data,
                "checked_at": datetime.now().isoformat(),
                "requires_alert": data["sisbajud_code"] in (98, 13),
            }
        return updated

    def _generate_alerts(self, assets: list[Asset]) -> list[Alert]:
        alerts = []
        for asset in assets:
            if asset.sisbajud_code == 98:
                alerts.append(
                    Alert(
                        id=f"alert_{asset.id}_no_response",
                        alert_type=AlertType.NAO_RESPOSTA,
                        severity=AlertSeverity.CRITICO,
                        subject=f"Não resposta SISBAJUD — {asset.institution}",
                        description=(
                            f"{asset.institution} não respondeu ao mandado SISBAJUD. "
                            f"Ativo: {asset.description}. "
                            f"Saldo declarado: R${asset.balance:,.2f}."
                        ),
                        institution=asset.institution,
                        created_at=datetime.now(),
                        asset_id=asset.id,
                        amount_at_risk=float(asset.balance),
                        legal_refs=[LEGAL_REFS["fraude_execucao"]],
                        requires_immediate_action=True,
                    )
                )
            if asset.is_suspect_drain:
                alerts.append(
                    Alert(
                        id=f"alert_{asset.id}_drain",
                        alert_type=AlertType.ESVAZIAMENTO_TATICO,
                        severity=AlertSeverity.CRITICO,
                        subject=f"Esvaziamento tático — {asset.institution}",
                        description=(
                            f"Variação suspeita em {asset.institution}: "
                            f"R${asset.previous_balance:,.2f} → R${asset.balance:,.2f} "
                            f"({asset.balance_variation * 100:.1f}%). "
                            f"Padrão consistente com ocultação patrimonial."
                        ),
                        institution=asset.institution,
                        created_at=datetime.now(),
                        asset_id=asset.id,
                        amount_at_risk=float(asset.previous_balance),
                        legal_refs=[
                            LEGAL_REFS["lavagem_dinheiro"],
                            LEGAL_REFS["desconsideracao_personalidade"],
                        ],
                        requires_immediate_action=True,
                    )
                )
        return alerts

    def _build_money_trail_summary(self, assets: list[Asset]) -> str:
        lines = ["=== WHOLE MONEY TRAIL — RESUMO ==="]
        for asset in assets:
            variation = ""
            if asset.previous_balance is not None:
                pct = asset.balance_variation * 100 if asset.balance_variation else 0
                variation = f" [VARIAÇÃO: {pct:.1f}%]"
            lines.append(
                f"  [{asset.risk_level.value}] {asset.institution} | "
                f"{asset.asset_type.value} | R${asset.balance:,.2f}{variation}"
            )
        return "\n".join(lines)

    def _log_report(self, report: BriefingReport) -> None:
        logger.info(
            f"[BRIEFING] Report complete — "
            f"Ativos: {len(report.assets)} | "
            f"Alertas críticos: {len(report.critical_alerts)} | "
            f"Total identificado: R${report.total_identified:,.2f} | "
            f"Em risco: R${report.total_at_risk:,.2f}"
        )
