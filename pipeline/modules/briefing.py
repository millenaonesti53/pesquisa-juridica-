"""
Briefing Module — Daily Intelligence Report.

Aggregates the Whole Money Trail, updates institution status based on
SISBAJUD response codes, generates automated alerts for FRAM/OSLO
non-response and BTG/Itaú tactical-emptying patterns.
"""

from __future__ import annotations

from datetime import datetime, date as date_type
from decimal import Decimal

from config.settings import LITIGATION_START_DATE, LEGAL_REFS, TACTICAL_EMPTYING_THRESHOLD, TACTICAL_EMPTYING_RATIO
from pipeline.models import (
    Alert,
    Asset,
    AssetStatus,
    Institution,
    PipelineReport,
    RiskLevel,
    SisbajudCode,
    WholeMoneyTrail,
)

MODULE_NAME = "BRIEFING"


def _default_assets() -> list[Asset]:
    """Return the canonical investigative dataset."""
    return [
        Asset(
            name="FRAM XIV FIP",
            institution="FRAM Capital",
            value_brl=Decimal("3877255.47"),
            asset_type="FIP",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_98,
            risk_level=RiskLevel.CRITICAL,
            notes="Side-pocket suspected; PL inconsistency detected; non-response Code 98.",
            creation_date="2019-06-01",
            is_post_litigation=False,
        ),
        Asset(
            name="LIG Itaú",
            institution="Itaú Unibanco",
            value_brl=Decimal("1250000.00"),
            asset_type="LIG",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_13,
            risk_level=RiskLevel.HIGH,
            notes="Responded zero balance; original value R$1.25M.",
        ),
        Asset(
            name="CDB BTG Pactual",
            institution="BTG Pactual",
            value_brl=Decimal("650758.60"),
            asset_type="CDB",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_13,
            risk_level=RiskLevel.HIGH,
            notes="Repeated zero-balance response with prior movement confirmed.",
        ),
        Asset(
            name="Bonifácio FIP",
            institution="Bonifácio Gestora",
            value_brl=Decimal("0.00"),
            asset_type="FIP",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_98,
            risk_level=RiskLevel.CRITICAL,
            notes="Created post-litigation — retroactive fraud indicator.",
            creation_date="2022-09-10",
            is_post_litigation=True,
        ),
        Asset(
            name="OSLO FIP",
            institution="OSLO Gestora",
            value_brl=Decimal("0.00"),
            asset_type="FIP",
            status=AssetStatus.UNRESPONSIVE,
            sisbajud_code=SisbajudCode.CODE_98,
            risk_level=RiskLevel.CRITICAL,
            notes="Persistent non-response — Code 98.",
        ),
        Asset(
            name="Ajaccio FIP",
            institution="Ajaccio Gestora",
            value_brl=Decimal("0.00"),
            asset_type="FIP",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_98,
            risk_level=RiskLevel.HIGH,
            notes="Temporal inconsistency detected in fund registration.",
        ),
        Asset(
            name="Conta Corrente Itaú",
            institution="Itaú Unibanco",
            value_brl=Decimal("5491.00"),
            asset_type="conta_corrente",
            status=AssetStatus.EMPTIED,
            sisbajud_code=SisbajudCode.CODE_13,
            risk_level=RiskLevel.CRITICAL,
            notes="Tactical emptying: R$469,575 → R$5,491 shortly before court order.",
        ),
    ]


def _default_institutions() -> list[Institution]:
    return [
        Institution(
            name="BTG Pactual",
            type="banco",
            sisbajud_code=SisbajudCode.CODE_13,
            last_response="2024-03-01T10:00:00",
            balance_history=[
                ("2024-01-15", Decimal("650758.60")),
                ("2024-02-01", Decimal("12000.00")),
                ("2024-03-01", Decimal("0.00")),
            ],
            risk_level=RiskLevel.CRITICAL,
        ),
        Institution(
            name="Itaú Unibanco",
            type="banco",
            sisbajud_code=SisbajudCode.CODE_13,
            last_response="2024-03-05T09:30:00",
            balance_history=[
                ("2024-01-10", Decimal("469575.00")),
                ("2024-02-20", Decimal("87400.00")),
                ("2024-03-05", Decimal("5491.00")),
            ],
            risk_level=RiskLevel.CRITICAL,
        ),
        Institution(
            name="FRAM Capital",
            type="gestora_fip",
            sisbajud_code=SisbajudCode.CODE_98,
            last_response=None,
            balance_history=[],
            risk_level=RiskLevel.CRITICAL,
        ),
        Institution(
            name="OSLO Gestora",
            type="gestora_fip",
            sisbajud_code=SisbajudCode.CODE_98,
            last_response=None,
            balance_history=[],
            risk_level=RiskLevel.CRITICAL,
        ),
    ]


class BriefingModule:
    """Produces the daily intelligence briefing for the legal investigation team."""

    def load_money_trail(self, investigation_date: str | None = None) -> WholeMoneyTrail:
        idate = investigation_date or datetime.utcnow().strftime("%Y-%m-%d")
        trail = WholeMoneyTrail(
            date=idate,
            assets=_default_assets(),
            institutions=_default_institutions(),
        )
        trail.compute_totals()
        return trail

    def update_institution_status(self, trail: WholeMoneyTrail) -> list[Institution]:
        for inst in trail.institutions:
            if inst.sisbajud_code == SisbajudCode.CODE_98:
                inst.risk_level = RiskLevel.CRITICAL
            elif inst.sisbajud_code == SisbajudCode.CODE_13:
                prev = inst.previous_balance()
                curr = inst.latest_balance()
                if prev and curr is not None and prev > TACTICAL_EMPTYING_THRESHOLD:
                    inst.risk_level = RiskLevel.CRITICAL
        return trail.institutions

    def generate_alerts(self, trail: WholeMoneyTrail) -> list[Alert]:
        alerts: list[Alert] = []

        # Non-response alerts (Code 98)
        non_responders = [
            i for i in trail.institutions if i.sisbajud_code == SisbajudCode.CODE_98
        ]
        for inst in non_responders:
            alerts.append(
                Alert(
                    level=RiskLevel.CRITICAL,
                    category="non_response",
                    description=(
                        f"{inst.name} não respondeu ao SISBAJUD (Código 98). "
                        "Ausência de resposta configura não cumprimento de ordem judicial."
                    ),
                    legal_refs=[LEGAL_REFS["art_171_cp"], LEGAL_REFS["art_792_cpc"]],
                    recommended_action=(
                        "Notificar juízo; requerer multa e eventual responsabilização criminal."
                    ),
                    institution=inst.name,
                    module=MODULE_NAME,
                )
            )

        # Tactical-emptying alerts
        for inst in trail.institutions:
            prev = inst.previous_balance()
            curr = inst.latest_balance()
            if prev is None or curr is None:
                continue
            drop = prev - curr
            ratio = drop / prev if prev else Decimal("0")
            if drop >= TACTICAL_EMPTYING_THRESHOLD and ratio >= TACTICAL_EMPTYING_RATIO:
                alerts.append(
                    Alert(
                        level=RiskLevel.CRITICAL,
                        category="tactical_emptying",
                        description=(
                            f"{inst.name}: esvaziamento tático detectado. "
                            f"Saldo caiu de R${prev:,.2f} para R${curr:,.2f} "
                            f"({ratio:.0%} de redução)."
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_792_cpc"],
                            LEGAL_REFS["art_50_cc"],
                            LEGAL_REFS["law_9613_98"],
                        ],
                        recommended_action=(
                            "Requerer bloqueio imediato e rastreamento de movimentação."
                        ),
                        institution=inst.name,
                        module=MODULE_NAME,
                    )
                )

        trail.alerts.extend(alerts)
        return alerts

    def generate_daily_report(
        self, trail: WholeMoneyTrail, alerts: list[Alert]
    ) -> PipelineReport:
        critical = sum(1 for a in alerts if a.level == RiskLevel.CRITICAL)
        high = sum(1 for a in alerts if a.level == RiskLevel.HIGH)
        status = "critical" if critical > 0 else ("warning" if high > 0 else "ok")

        return PipelineReport(
            module=MODULE_NAME,
            status=status,
            findings={
                "investigation_date": trail.date,
                "total_assets": len(trail.assets),
                "total_tracked_brl": str(trail.total_tracked),
                "total_blocked_brl": str(trail.total_blocked),
                "total_evaded_brl": str(trail.total_evaded),
                "non_responders": [
                    i.name
                    for i in trail.institutions
                    if i.sisbajud_code == SisbajudCode.CODE_98
                ],
                "tactical_emptying_detected": [
                    i.name
                    for i in trail.institutions
                    if i.sisbajud_code == SisbajudCode.CODE_13
                    and i.previous_balance()
                    and i.latest_balance() is not None
                    and (i.previous_balance() - i.latest_balance())  # type: ignore[operator]
                    >= TACTICAL_EMPTYING_THRESHOLD
                ],
            },
            alerts=alerts,
            recommendations=[
                "Notificar FRAM Capital e OSLO Gestora pelo não cumprimento (Cód. 98).",
                "Requerer rastreamento de movimentações de BTG Pactual e Itaú.",
                "Considerar representação ao COAF sobre movimentações suspeitas.",
                "Solicitar quebra de sigilo bancário complementar.",
            ],
        )

    def run(self, investigation_date: str | None = None) -> tuple[WholeMoneyTrail, PipelineReport]:
        trail = self.load_money_trail(investigation_date)
        self.update_institution_status(trail)
        alerts = self.generate_alerts(trail)
        report = self.generate_daily_report(trail, alerts)
        return trail, report
