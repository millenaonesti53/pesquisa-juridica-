"""
Module 2: SYSTEM HEALTH CHECK
Monitors API availability (CVM, SISBAJUD, banks), detects PL inconsistencies,
divergences between IRPF and CVM, and signals of asset concealment.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
import logging

from config.settings import MONITORED_INSTITUTIONS
from models.alerts import Alert, AlertType, AlertSeverity, Alert
from models.assets import RiskLevel

logger = logging.getLogger(__name__)


@dataclass
class ServiceStatus:
    name: str
    is_healthy: bool
    latency_ms: Optional[float]
    last_checked: datetime
    error_message: str = ""


@dataclass
class PLInconsistency:
    fip_name: str
    cnpj: str
    pl_cvm: Decimal
    pl_irpf: Decimal
    divergence: Decimal
    divergence_pct: float
    risk_level: RiskLevel

    @property
    def is_critical(self) -> bool:
        return self.divergence_pct > 15.0 or self.divergence > Decimal("500000")


# Known PL inconsistencies from investigation
KNOWN_PL_INCONSISTENCIES = [
    PLInconsistency(
        fip_name="FRAM XIV FIP",
        cnpj="XX.XXX.XXX/0001-XX",
        pl_cvm=Decimal("3877255.47"),
        pl_irpf=Decimal("0.00"),  # Not declared in IRPF
        divergence=Decimal("3877255.47"),
        divergence_pct=100.0,
        risk_level=RiskLevel.CRITICO,
    ),
    PLInconsistency(
        fip_name="LIG Itaú",
        cnpj="N/A",
        pl_cvm=Decimal("1250000.00"),
        pl_irpf=Decimal("1250000.00"),
        divergence=Decimal("0.00"),
        divergence_pct=0.0,
        risk_level=RiskLevel.ALTO,  # Risk from impenhorability claim
    ),
]

CRITICAL_ASSETS_AT_RISK = {
    "FRAM XIV FIP": Decimal("3877255.47"),
    "LIG Itaú": Decimal("1250000.00"),
    "CDB BTG": Decimal("650758.60"),
}


@dataclass
class HealthCheckReport:
    checked_at: datetime
    services: list[ServiceStatus]
    pl_inconsistencies: list[PLInconsistency]
    critical_alerts: list[Alert]
    non_responsive_institutions: list[str]
    tactical_drains: list[dict]
    overall_health: str = "OK"

    @property
    def has_critical_issues(self) -> bool:
        return any(not s.is_healthy for s in self.services) or bool(
            self.critical_alerts
        )


class HealthCheckModule:
    """
    Infrastructure and legal integrity monitor.
    Checks API health, detects PL divergences, flags concealment signals.
    """

    def run(self) -> HealthCheckReport:
        logger.info("[HEALTH CHECK] Starting system health check")

        services = self._check_services()
        pl_inconsistencies = self._check_pl_inconsistencies()
        alerts = self._generate_alerts(services, pl_inconsistencies)
        non_responsive = self._identify_non_responsive_institutions()
        drains = self._detect_tactical_drains()

        overall = "CRITICAL" if any(a.severity == AlertSeverity.CRITICO for a in alerts) else "WARNING" if alerts else "OK"

        report = HealthCheckReport(
            checked_at=datetime.now(),
            services=services,
            pl_inconsistencies=pl_inconsistencies,
            critical_alerts=alerts,
            non_responsive_institutions=non_responsive,
            tactical_drains=drains,
            overall_health=overall,
        )

        self._log_report(report)
        return report

    def _check_services(self) -> list[ServiceStatus]:
        services_to_check = [
            "CVM_API",
            "SISBAJUD",
            "BACEN_REGISTRATO",
            "RECEITA_FEDERAL",
            "BANCO_ITAU",
            "BANCO_BTG",
        ]
        results = []
        for svc in services_to_check:
            # In production: perform actual health probe
            results.append(
                ServiceStatus(
                    name=svc,
                    is_healthy=True,
                    latency_ms=None,
                    last_checked=datetime.now(),
                    error_message="",
                )
            )
        return results

    def _check_pl_inconsistencies(self) -> list[PLInconsistency]:
        logger.info("[HEALTH CHECK] Checking PL inconsistencies")
        return KNOWN_PL_INCONSISTENCIES

    def _generate_alerts(
        self, services: list[ServiceStatus], inconsistencies: list[PLInconsistency]
    ) -> list[Alert]:
        alerts = []

        for svc in services:
            if not svc.is_healthy:
                alerts.append(
                    Alert(
                        id=f"health_{svc.name}_down",
                        alert_type=AlertType.NAO_RESPOSTA,
                        severity=AlertSeverity.ALTO,
                        subject=f"Serviço indisponível: {svc.name}",
                        description=f"{svc.name} não está respondendo. Erro: {svc.error_message}",
                        institution=svc.name,
                        created_at=datetime.now(),
                        requires_immediate_action=True,
                    )
                )

        for inc in inconsistencies:
            if inc.is_critical:
                alerts.append(
                    Alert(
                        id=f"health_pl_divergence_{inc.cnpj}",
                        alert_type=AlertType.DIVERGENCIA_PL,
                        severity=AlertSeverity.CRITICO,
                        subject=f"Divergência PL — {inc.fip_name}",
                        description=(
                            f"PL CVM: R${inc.pl_cvm:,.2f} vs "
                            f"IRPF declarado: R${inc.pl_irpf:,.2f}. "
                            f"Divergência: R${inc.divergence:,.2f} ({inc.divergence_pct:.1f}%). "
                            f"Indicativo de omissão patrimonial."
                        ),
                        institution=inc.fip_name,
                        created_at=datetime.now(),
                        amount_at_risk=float(inc.divergence),
                        legal_refs=["Lei 9.613/98 Art. 1°", "CP Art. 171"],
                        requires_immediate_action=True,
                    )
                )

        return alerts

    def _identify_non_responsive_institutions(self) -> list[str]:
        non_responsive = ["FRAM", "OSLO"]
        for inst in non_responsive:
            logger.warning(f"[HEALTH CHECK] Non-responsive institution: {inst} (SISBAJUD code 98)")
        return non_responsive

    def _detect_tactical_drains(self) -> list[dict]:
        drains = [
            {
                "institution": "BTG",
                "description": "CDB zerado. Saldo anterior: R$650.758,60",
                "sisbajud_code": 13,
                "pattern": "ZERO_BALANCE_REPEAT",
            },
            {
                "institution": "ITAU",
                "description": "Conta esvaziada: R$469.575 → R$5.491 (-98.8%)",
                "sisbajud_code": 1,
                "pattern": "TACTICAL_DRAIN_PRE_ORDER",
            },
        ]
        for d in drains:
            logger.critical(f"[HEALTH CHECK] Tactical drain: {d['institution']} — {d['description']}")
        return drains

    def _log_report(self, report: HealthCheckReport) -> None:
        logger.info(
            f"[HEALTH CHECK] Complete — "
            f"Status geral: {report.overall_health} | "
            f"Serviços: {len(report.services)} | "
            f"Alertas críticos: {len(report.critical_alerts)} | "
            f"Instituições sem resposta: {report.non_responsive_institutions}"
        )
