"""
Dependency Check Module — Corporate Cognitive Pipeline.

Analyses structural and temporal dependencies between assets, detecting:
    - Post-litigation FIP creation (Bonifácio FIP)
    - Side-pocket patterns in illiquid FIPs (FRAM XIV)
    - Regulatory / statute amendments suspiciously timed with litigation
    - Temporal inconsistencies in fund registration data (Ajaccio FIP)

Legal framework applied:
    - Art. 792 CPC  — Fraude à Execução
    - Art. 171 CP   — Estelionato
    - Art. 50 CC    — Desconsideração da Personalidade Jurídica
    - Lei 9.613/98  — Lavagem de Dinheiro
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from config.settings import (
    LEGAL_REFS,
    LITIGATION_START_DATE,
    SIDE_POCKET_ILLIQUID_RATIO,
)
from pipeline.models import (
    Alert,
    Asset,
    AssetStatus,
    PipelineReport,
    RiskLevel,
    SisbajudCode,
    WholeMoneyTrail,
)

MODULE_NAME = "DEPENDENCY_CHECK"

# Simulated regulatory events sourced from CVM filings (no real API calls)
_REGULATORY_EVENTS: list[dict] = [
    {
        "asset_name": "FRAM XIV FIP",
        "event_type": "classe_j_creation",
        "event_date": "2022-04-18",
        "description": (
            "Criação de Classe J (cotas subordinadas sem liquidez) no FRAM XIV FIP, "
            "28 dias após o início do litígio (2022-03-15). "
            "Classe J permite reclassificação de ativos como ilíquidos, "
            "bloqueando a penhora judicial."
        ),
        "risk_level": RiskLevel.CRITICAL,
    },
    {
        "asset_name": "Ajaccio FIP",
        "event_type": "statute_amendment",
        "event_date": "2022-03-29",
        "description": (
            "Alteração estatutária do Ajaccio FIP registrada na CVM em 2022-03-29, "
            "apenas 14 dias após o início do litígio. "
            "Alterações incluem mudança de política de resgate e adição de cláusula "
            "de lock-up de 36 meses para novos cotistas."
        ),
        "risk_level": RiskLevel.HIGH,
    },
    {
        "asset_name": "Bonifácio FIP",
        "event_type": "fund_creation",
        "event_date": "2022-09-10",
        "description": (
            "Constituição do Bonifácio FIP registrada na CVM em 2022-09-10, "
            "179 dias após o início do litígio (2022-03-15). "
            "Estrutura societária replica parcialmente a do OSLO FIP, "
            "sugerindo continuidade por veículo diverso."
        ),
        "risk_level": RiskLevel.CRITICAL,
    },
]

# Simulated temporal inconsistency data
_TEMPORAL_INCONSISTENCIES: list[dict] = [
    {
        "asset_name": "Ajaccio FIP",
        "claimed_start_date": "2021-09-14",
        "first_documented_activity": "2021-07-02",
        "description": (
            "Ajaccio FIP declara data de início em 2021-09-14, porém registros "
            "de movimentação financeira foram identificados a partir de 2021-07-02 "
            "— 74 dias antes da data oficial. Atividade pré-registro é "
            "juridicamente impossível e aponta para adulteração documental."
        ),
        "risk_level": RiskLevel.HIGH,
    },
]

# Simulated side-pocket data (illiquid fraction per FIP)
_SIDE_POCKET_DATA: dict[str, Decimal] = {
    "FRAM XIV FIP": Decimal("0.63"),   # 63% illiquid — well above the 30% threshold
    "Bonifácio FIP": Decimal("1.00"),  # 100% illiquid — fully opaque
    "OSLO FIP": Decimal("1.00"),       # 100% illiquid — fully opaque
    "Ajaccio FIP": Decimal("0.42"),    # 42% illiquid — above threshold
}


class DependencyCheckModule:
    """Checks structural/temporal dependencies to detect fraud-construction patterns."""

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def check_fip_creation_dates(self, assets: list[Asset]) -> list[Alert]:
        """Detect FIPs created after litigation start (retroactive fraud indicator).

        Args:
            assets: List of tracked :class:`Asset` objects.

        Returns:
            List of :class:`Alert` objects for post-litigation creations.
        """
        litigation_start = date.fromisoformat(LITIGATION_START_DATE)
        alerts: list[Alert] = []

        for asset in assets:
            if asset.asset_type != "FIP":
                continue
            if not asset.creation_date:
                continue
            creation = date.fromisoformat(asset.creation_date)
            if creation > litigation_start:
                delta_days = (creation - litigation_start).days
                alerts.append(
                    Alert(
                        level=RiskLevel.CRITICAL,
                        category="post_litigation_fip_creation",
                        description=(
                            f"{asset.name} constituído em {asset.creation_date}, "
                            f"{delta_days} dias após o início do litígio "
                            f"({LITIGATION_START_DATE}). Criação pós-litígio configura "
                            f"indicador de fraude retroativa; o fundo pode ter sido "
                            f"criado para dissipação ou ocultação patrimonial."
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_792_cpc"],
                            LEGAL_REFS["art_50_cc"],
                            LEGAL_REFS["art_171_cp"],
                        ],
                        recommended_action=(
                            f"Requerer ao juízo a desconsideração do {asset.name} como "
                            f"veículo de fraude. Investigar beneficiários finais e cotistas. "
                            f"Verificar se há movimentação de ativos do réu para este fundo."
                        ),
                        institution=asset.institution,
                        asset=asset,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def detect_side_pockets(self, assets: list[Asset]) -> list[Alert]:
        """Detect suspicious illiquidity claims (side-pocket patterns).

        A side-pocket is a mechanism by which an asset manager segregates
        illiquid/hard-to-value assets from the main fund portfolio. When the
        illiquid fraction exceeds the configured threshold, it may be used
        as a tactic to avoid judicial attachment.

        Args:
            assets: List of tracked :class:`Asset` objects.

        Returns:
            List of :class:`Alert` objects for side-pocket detections.
        """
        alerts: list[Alert] = []
        for asset in assets:
            illiquid_fraction = _SIDE_POCKET_DATA.get(asset.name)
            if illiquid_fraction is None:
                continue
            if illiquid_fraction >= SIDE_POCKET_ILLIQUID_RATIO:
                level = (
                    RiskLevel.CRITICAL
                    if illiquid_fraction >= Decimal("0.60")
                    else RiskLevel.HIGH
                )
                alerts.append(
                    Alert(
                        level=level,
                        category="side_pocket_suspected",
                        description=(
                            f"{asset.name}: fração ilíquida = {float(illiquid_fraction):.0%} "
                            f"(limiar: {float(SIDE_POCKET_ILLIQUID_RATIO):.0%}). "
                            f"Percentual elevado de ativos ilíquidos pode indicar uso de "
                            f"side-pocket como mecanismo de subtração à penhora judicial. "
                            f"Valor total em risco: R$ {asset.value_brl:,.2f}."
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_171_cp"],
                            LEGAL_REFS["art_792_cpc"],
                            LEGAL_REFS["law_9613_98"],
                        ],
                        recommended_action=(
                            f"Solicitar laudo pericial sobre composição da carteira do {asset.name}. "
                            f"Requerer acesso à lista de ativos ilíquidos segregados. "
                            f"Verificar se houve reclassificação de ativos após o início do litígio."
                        ),
                        institution=asset.institution,
                        asset=asset,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def check_regulatory_changes(self, assets: list[Asset]) -> list[Alert]:
        """Detect regulatory / statute changes suspiciously timed with litigation.

        Args:
            assets: List of tracked :class:`Asset` objects.

        Returns:
            List of :class:`Alert` objects for suspicious regulatory changes.
        """
        asset_map = {a.name: a for a in assets}
        litigation_start = date.fromisoformat(LITIGATION_START_DATE)
        alerts: list[Alert] = []

        for event in _REGULATORY_EVENTS:
            asset = asset_map.get(event["asset_name"])
            event_date = date.fromisoformat(event["event_date"])
            days_after = (event_date - litigation_start).days

            # Flag if the event occurred within 180 days of litigation start
            if days_after >= 0 and days_after <= 180:
                alerts.append(
                    Alert(
                        level=event["risk_level"],
                        category=f"regulatory_change_{event['event_type']}",
                        description=(
                            f"{event['asset_name']} — {event['description']} "
                            f"(Evento ocorrido {days_after} dias após início do litígio.)"
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_792_cpc"],
                            LEGAL_REFS["art_171_cp"],
                        ],
                        recommended_action=(
                            "Requerer ao juízo declaração de ineficácia da alteração. "
                            "Solicitar CVM expediente de fiscalização emergencial."
                        ),
                        institution=asset.institution if asset else None,
                        asset=asset,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def verify_temporal_consistency(self, assets: list[Asset]) -> list[Alert]:
        """Detect impossible temporal sequences in fund records.

        Checks for activity dates that predate official registration — a clear
        indicator of document manipulation.

        Args:
            assets: List of tracked :class:`Asset` objects.

        Returns:
            List of :class:`Alert` objects for temporal inconsistencies.
        """
        asset_map = {a.name: a for a in assets}
        alerts: list[Alert] = []

        for inc in _TEMPORAL_INCONSISTENCIES:
            asset = asset_map.get(inc["asset_name"])
            claimed = date.fromisoformat(inc["claimed_start_date"])
            first_activity = date.fromisoformat(inc["first_documented_activity"])
            gap_days = (claimed - first_activity).days

            alerts.append(
                Alert(
                    level=inc["risk_level"],
                    category="temporal_inconsistency",
                    description=(
                        f"{inc['asset_name']}: {inc['description']} "
                        f"(Inconsistência temporal de {gap_days} dias.)"
                    ),
                    legal_refs=[
                        LEGAL_REFS["art_171_cp"],
                        LEGAL_REFS["art_792_cpc"],
                    ],
                    recommended_action=(
                        "Solicitar perícia documental nos registros CVM e Cartório de RTD. "
                        "Verificar autenticidade dos documentos de constituição do fundo."
                    ),
                    institution=asset.institution if asset else None,
                    asset=asset,
                    module=MODULE_NAME,
                )
            )
        return alerts

    def run(self, trail: WholeMoneyTrail) -> PipelineReport:
        """Execute all dependency checks and return a consolidated report.

        Args:
            trail: The current :class:`WholeMoneyTrail`.

        Returns:
            A :class:`PipelineReport` with all findings.
        """
        alerts: list[Alert] = []

        creation_alerts = self.check_fip_creation_dates(trail.assets)
        side_pocket_alerts = self.detect_side_pockets(trail.assets)
        regulatory_alerts = self.check_regulatory_changes(trail.assets)
        temporal_alerts = self.verify_temporal_consistency(trail.assets)

        alerts.extend(creation_alerts)
        alerts.extend(side_pocket_alerts)
        alerts.extend(regulatory_alerts)
        alerts.extend(temporal_alerts)

        critical_count = sum(1 for a in alerts if a.level == RiskLevel.CRITICAL)
        high_count = sum(1 for a in alerts if a.level == RiskLevel.HIGH)
        status = (
            "critical" if critical_count > 0
            else "warning" if high_count > 0
            else "ok"
        )

        return PipelineReport(
            module=MODULE_NAME,
            status=status,
            findings={
                "post_litigation_creations": len(creation_alerts),
                "side_pockets_detected": len(side_pocket_alerts),
                "regulatory_changes": len(regulatory_alerts),
                "temporal_inconsistencies": len(temporal_alerts),
                "affected_assets": list({
                    a.asset.name for a in alerts if a.asset is not None
                }),
            },
            alerts=alerts,
            recommendations=[
                "Peticionar anulação do Bonifácio FIP por fraude à execução (Art. 792 CPC).",
                "Requerer laudo pericial sobre side-pocket do FRAM XIV FIP.",
                "Solicitar expediente CVM de fiscalização emergencial do Ajaccio FIP.",
                "Investigar sobreposição societária entre OSLO FIP e Bonifácio FIP.",
                "Requerer declaração de ineficácia das alterações estatutárias pós-litígio.",
            ],
        )


# ---------------------------------------------------------------------------
# Module self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from pipeline.modules.briefing import BriefingModule

    trail, _ = BriefingModule().run()
    module = DependencyCheckModule()
    report = module.run(trail)

    print(f"=== DEPENDENCY CHECK SELF-TEST ===")
    print(f"Status: {report.status}")
    print(f"Findings: {report.findings}")
    print(f"Alerts ({len(report.alerts)}):")
    for a in report.alerts:
        print(f"  [{a.level.name}] {a.category}: {a.description[:100]}...")
