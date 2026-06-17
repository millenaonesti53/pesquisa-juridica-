"""
System Health Check Module.

Monitors simulated CVM/SISBAJUD API status, detects PL inconsistencies,
balance anomalies, and non-response patterns at the infrastructure level.
"""

from __future__ import annotations

import math
from decimal import Decimal

from config.settings import ANOMALY_Z_SCORE, LEGAL_REFS, TACTICAL_EMPTYING_THRESHOLD, TACTICAL_EMPTYING_RATIO
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

MODULE_NAME = "SYSTEM_HEALTH_CHECK"

# Simulated expected PL values from last CVM filing
_EXPECTED_PL: dict[str, Decimal] = {
    "FRAM XIV FIP": Decimal("3877255.47"),
    "Bonifácio FIP": Decimal("0.00"),
    "OSLO FIP": Decimal("0.00"),
    "Ajaccio FIP": Decimal("0.00"),
}

# Simulated API health map
_API_STATUS: dict[str, str] = {
    "CVM_API": "online",
    "SISBAJUD_API": "online",
    "DATADOG": "online",
    "SENTRY": "online",
    "BTG_INTEGRATOR": "degraded",
    "ITAU_INTEGRATOR": "degraded",
    "FRAM_INTEGRATOR": "offline",
    "OSLO_INTEGRATOR": "offline",
}


class SystemHealthCheck:
    """Verifies infrastructure health and detects fraud-indicative data anomalies."""

    def check_api_status(self) -> dict[str, str]:
        return dict(_API_STATUS)

    def detect_pl_inconsistencies(self, assets: list[Asset]) -> list[Alert]:
        alerts: list[Alert] = []
        for asset in assets:
            expected = _EXPECTED_PL.get(asset.name)
            if expected is None:
                continue
            if expected == Decimal("0.00"):
                continue
            # Flag if current value diverges from the expected CVM-filed PL by >5%
            if expected > 0:
                divergence = abs(asset.value_brl - expected) / expected
                if divergence > Decimal("0.05"):
                    alerts.append(
                        Alert(
                            level=RiskLevel.CRITICAL,
                            category="pl_inconsistency",
                            description=(
                                f"{asset.name}: PL declarado diverge do valor CVM. "
                                f"Esperado R${expected:,.2f}, "
                                f"atual R${asset.value_brl:,.2f} "
                                f"(divergência {float(divergence):.1%})."
                            ),
                            legal_refs=[
                                LEGAL_REFS["art_171_cp"],
                                LEGAL_REFS["fatca_crs"],
                            ],
                            recommended_action=(
                                "Solicitar extrato CVM atualizado e confrontar com IRPF."
                            ),
                            institution=asset.institution,
                            asset=asset,
                            module=MODULE_NAME,
                        )
                    )
        return alerts

    def detect_balance_anomalies(self, institutions: list[Institution]) -> list[Alert]:
        alerts: list[Alert] = []
        for inst in institutions:
            if len(inst.balance_history) < 2:
                continue
            values = [float(v) for _, v in inst.balance_history]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std_dev = math.sqrt(variance) if variance > 0 else 0.0
            latest = values[-1]
            z_latest = (latest - mean) / std_dev if std_dev > 0 else 0.0
            is_statistical_anomaly = std_dev > 0 and z_latest < -ANOMALY_Z_SCORE

            # Flag if any consecutive pair meets both absolute and proportional thresholds
            worst_prev = Decimal("0")
            worst_curr = Decimal("0")
            worst_drop = Decimal("0")
            worst_ratio = Decimal("0")
            is_tactical_drop = False
            for i in range(1, len(values)):
                pv = Decimal(str(values[i - 1]))
                cv = Decimal(str(values[i]))
                if pv <= 0:
                    continue
                d = pv - cv
                r = d / pv
                if d >= TACTICAL_EMPTYING_THRESHOLD and r >= TACTICAL_EMPTYING_RATIO:
                    is_tactical_drop = True
                    if d > worst_drop:
                        worst_drop, worst_prev, worst_curr, worst_ratio = d, pv, cv, r

            if is_statistical_anomaly or is_tactical_drop:
                alerts.append(
                    Alert(
                        level=RiskLevel.CRITICAL,
                        category="balance_anomaly",
                        description=(
                            f"{inst.name}: anomalia de saldo detectada. "
                            f"Maior queda: R${worst_prev:,.2f} → R${worst_curr:,.2f} "
                            f"({float(worst_ratio):.0%} de redução). "
                            f"Z-score final={z_latest:.2f}, média histórica R${mean:,.2f}."
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_792_cpc"],
                            LEGAL_REFS["law_9613_98"],
                        ],
                        recommended_action=(
                            "Requerer extrato completo e rastreamento de TED/DOC."
                        ),
                        institution=inst.name,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def detect_non_responses(self, institutions: list[Institution]) -> list[Alert]:
        alerts: list[Alert] = []
        for inst in institutions:
            if inst.sisbajud_code == SisbajudCode.CODE_98:
                alerts.append(
                    Alert(
                        level=RiskLevel.CRITICAL,
                        category="sisbajud_non_response",
                        description=(
                            f"{inst.name} retornou Código 98 (ausência de resposta). "
                            "Infraestrutura do integrador reporta status: "
                            f"{_API_STATUS.get(inst.name.upper().replace(' ', '_') + '_INTEGRATOR', 'desconhecido')}."
                        ),
                        legal_refs=[LEGAL_REFS["art_171_cp"], LEGAL_REFS["art_792_cpc"]],
                        recommended_action=(
                            "Registrar em ata; acionar juízo para impor astreintes."
                        ),
                        institution=inst.name,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def run(self, trail: WholeMoneyTrail) -> PipelineReport:
        api_status = self.check_api_status()
        alerts: list[Alert] = []

        alerts.extend(self.detect_pl_inconsistencies(trail.assets))
        alerts.extend(self.detect_balance_anomalies(trail.institutions))
        alerts.extend(self.detect_non_responses(trail.institutions))

        offline_apis = [k for k, v in api_status.items() if v == "offline"]
        degraded_apis = [k for k, v in api_status.items() if v == "degraded"]

        critical_count = sum(1 for a in alerts if a.level == RiskLevel.CRITICAL)
        status = "critical" if (critical_count > 0 or offline_apis) else (
            "warning" if degraded_apis else "ok"
        )

        return PipelineReport(
            module=MODULE_NAME,
            status=status,
            findings={
                "api_status": api_status,
                "offline_apis": offline_apis,
                "degraded_apis": degraded_apis,
                "pl_inconsistencies": sum(
                    1 for a in alerts if a.category == "pl_inconsistency"
                ),
                "balance_anomalies": sum(
                    1 for a in alerts if a.category == "balance_anomaly"
                ),
                "non_responses": sum(
                    1 for a in alerts if a.category == "sisbajud_non_response"
                ),
            },
            alerts=alerts,
            recommendations=[
                "Investigar integradores FRAM e OSLO offline.",
                "Solicitar logs completos BTG/Itaú ao SISBAJUD.",
                "Confrontar PL declarado na CVM com extratos físicos do FRAM XIV FIP.",
            ],
        )
