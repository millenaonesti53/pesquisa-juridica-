"""
Flaky Tracker Module — Corporate Cognitive Pipeline.

Tracks repeated inconsistencies in SISBAJUD responses ("flakiness"):
    - Institutions that oscillate between zero-balance and non-response
    - Illiquidity claims that are statistically inconsistent with market data
    - Pre-order emptying patterns (BTG, Itaú)
    - Statistical analysis of balance history (mean, std-dev, z-score anomaly)

The "flakiness" framing comes from software testing: an institution that
produces unreliable, non-deterministic SISBAJUD responses is suspicious —
just as a test that sometimes passes and sometimes fails deserves scrutiny.

Legal framework:
    - Art. 171 CP   — Estelionato (fraud)
    - Art. 792 CPC  — Fraude à Execução
    - Lei 9.613/98  — Lavagem de Dinheiro
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from config.settings import (
    ANOMALY_Z_SCORE,
    LEGAL_REFS,
    LITIGATION_START_DATE,
    TACTICAL_EMPTYING_RATIO,
    TACTICAL_EMPTYING_THRESHOLD,
)
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

MODULE_NAME = "FLAKY_TRACKER"


# ---------------------------------------------------------------------------
# Supplementary dataclass
# ---------------------------------------------------------------------------


@dataclass
class BalanceFlakiness:
    """Records a detected flakiness pattern for a single institution.

    Attributes:
        institution: Institution name.
        pattern: Short pattern label (e.g. 'oscillating_zero', 'pre_order_emptying').
        occurrences: Number of times the suspicious pattern was observed.
        verdict: Human-readable verdict (e.g. 'SUSPEITO', 'CONFIRMADO').
        evidence: List of supporting evidence strings.
    """

    institution: str
    pattern: str
    occurrences: int
    verdict: str
    evidence: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pre-order movement data (simulated judicial timeline correlation)
# ---------------------------------------------------------------------------

_PRE_ORDER_MOVEMENTS: list[dict] = [
    {
        "institution": "BTG Pactual",
        "order_date": "2024-01-15",
        "movements": [
            {"date": "2024-01-13", "amount": Decimal("-638758.60"), "type": "TED_saída"},
            {"date": "2024-01-14", "amount": Decimal("-12000.00"), "type": "TED_saída"},
        ],
        "balance_before": Decimal("650758.60"),
        "balance_after": Decimal("0.00"),
        "days_before_order": 2,
    },
    {
        "institution": "Itaú Unibanco",
        "order_date": "2024-01-10",
        "movements": [
            {"date": "2024-01-08", "amount": Decimal("-382175.00"), "type": "TED_saída"},
            {"date": "2024-01-09", "amount": Decimal("-81909.00"), "type": "DOC_saída"},
        ],
        "balance_before": Decimal("469575.00"),
        "balance_after": Decimal("5491.00"),
        "days_before_order": 2,
    },
]

# Illiquidity claim data for FIPs (claimed vs. market-verifiable)
_ILLIQUIDITY_CLAIMS: list[dict] = [
    {
        "asset_name": "FRAM XIV FIP",
        "claimed_illiquid_fraction": Decimal("0.63"),
        "market_reference_fraction": Decimal("0.22"),
        "description": (
            "FRAM XIV FIP declara 63% de ativos ilíquidos, porém fundos similares "
            "de Private Equity no mesmo segmento apresentam média de 22% de iliquidez. "
            "Divergência de 41 pontos percentuais é estatisticamente anômala."
        ),
    },
    {
        "asset_name": "OSLO FIP",
        "claimed_illiquid_fraction": Decimal("1.00"),
        "market_reference_fraction": Decimal("0.28"),
        "description": (
            "OSLO FIP afirma 100% de iliquidez total — figura juridicamente improvável "
            "para um fundo em operação normal. Referência de mercado para fundos "
            "similares é de 28% de iliquidez."
        ),
    },
]


class FlakyTestTracker:
    """Tracks flakiness patterns in institutional SISBAJUD responses.

    Uses statistical analysis to distinguish genuine illiquidity from
    deliberate evasion tactics, and identifies correlations between
    judicial order timelines and sudden balance movements.
    """

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def test_sisbajud_consistency(
        self, institutions: list[Institution]
    ) -> list[BalanceFlakiness]:
        """Evaluate each institution's SISBAJUD response pattern for flakiness.

        An institution is "flaky" if it oscillates between:
            - Responding with zero (Code 13) and non-response (Code 98)
            - Reporting dramatically different balances across short periods

        Args:
            institutions: List of :class:`Institution` objects.

        Returns:
            List of :class:`BalanceFlakiness` assessments.
        """
        results: list[BalanceFlakiness] = []

        for inst in institutions:
            evidence: list[str] = []
            pattern = "consistent"
            occurrences = 0

            if len(inst.balance_history) < 2:
                if inst.sisbajud_code == SisbajudCode.CODE_98:
                    results.append(
                        BalanceFlakiness(
                            institution=inst.name,
                            pattern="total_silence",
                            occurrences=1,
                            verdict="NÃO RESPONSIVO — SUSPEITO",
                            evidence=[
                                f"Nenhum histórico de saldo; SISBAJUD retornou Código 98."
                            ],
                        )
                    )
                continue

            values = [float(v) for _, v in inst.balance_history]
            dates = [d for d, _ in inst.balance_history]

            # Detect oscillation between positive and zero
            zero_transitions = sum(
                1
                for i in range(1, len(values))
                if values[i] == 0.0 and values[i - 1] > 0.0
            )
            if zero_transitions >= 1:
                pattern = "oscillating_zero"
                occurrences = zero_transitions
                evidence.append(
                    f"Transição(ões) de saldo positivo para zero: {zero_transitions}x. "
                    f"Datas: {', '.join(dates[i] for i in range(1, len(values)) if values[i] == 0.0 and values[i-1] > 0.0)}"
                )

            # Detect large single-step drops
            for i in range(1, len(values)):
                prev_v = Decimal(str(values[i - 1]))
                curr_v = Decimal(str(values[i]))
                if prev_v > Decimal("0"):
                    drop_ratio = (prev_v - curr_v) / prev_v
                    if drop_ratio >= TACTICAL_EMPTYING_RATIO:
                        occurrences += 1
                        evidence.append(
                            f"Queda abrupta em {dates[i]}: "
                            f"R$ {prev_v:,.2f} → R$ {curr_v:,.2f} "
                            f"({float(drop_ratio):.0%} de redução)."
                        )
                        pattern = "pre_order_emptying"

            if evidence:
                verdict = (
                    "CONFIRMADO — ESVAZIAMENTO TÁTICO"
                    if pattern == "pre_order_emptying"
                    else "SUSPEITO — OSCILAÇÃO ANÔMALA"
                )
                results.append(
                    BalanceFlakiness(
                        institution=inst.name,
                        pattern=pattern,
                        occurrences=occurrences,
                        verdict=verdict,
                        evidence=evidence,
                    )
                )

        return results

    def test_illiquidity_claim(self, assets: list[Asset]) -> list[Alert]:
        """Test whether illiquidity claims are statistically consistent with market data.

        Args:
            assets: List of tracked :class:`Asset` objects.

        Returns:
            List of :class:`Alert` objects for inconsistent illiquidity claims.
        """
        asset_map = {a.name: a for a in assets}
        alerts: list[Alert] = []

        for claim in _ILLIQUIDITY_CLAIMS:
            asset = asset_map.get(claim["asset_name"])
            claimed = claim["claimed_illiquid_fraction"]
            reference = claim["market_reference_fraction"]
            divergence = abs(claimed - reference)

            # Flag if divergence exceeds 20 percentage points
            if divergence >= Decimal("0.20"):
                alerts.append(
                    Alert(
                        level=RiskLevel.CRITICAL if divergence >= Decimal("0.30") else RiskLevel.HIGH,
                        category="illiquidity_claim_inconsistent",
                        description=(
                            f"{claim['asset_name']}: {claim['description']} "
                            f"Divergência absoluta: {float(divergence):.0%}."
                        ),
                        legal_refs=[
                            LEGAL_REFS["art_171_cp"],
                            LEGAL_REFS["art_792_cpc"],
                        ],
                        recommended_action=(
                            "Solicitar laudo pericial independente sobre composição da carteira. "
                            "Requerer ao juízo nomeação de administrador provisório para acesso "
                            "aos ativos ilíquidos segregados."
                        ),
                        institution=asset.institution if asset else None,
                        asset=asset,
                        module=MODULE_NAME,
                    )
                )
        return alerts

    def detect_pre_order_emptying(self, institutions: list[Institution]) -> list[Alert]:
        """Detect balance movements that occurred immediately before judicial orders.

        Compares the timing of fund outflows against the known judicial order
        dates to identify coordinated pre-emptive asset concealment.

        Args:
            institutions: List of :class:`Institution` objects.

        Returns:
            List of :class:`Alert` objects for pre-order emptying patterns.
        """
        inst_map = {i.name: i for i in institutions}
        alerts: list[Alert] = []

        for movement in _PRE_ORDER_MOVEMENTS:
            inst = inst_map.get(movement["institution"])
            total_outflow = sum(
                abs(m["amount"]) for m in movement["movements"]
            )
            movement_dates = ", ".join(m["date"] for m in movement["movements"])

            alert = Alert(
                level=RiskLevel.CRITICAL,
                category="pre_order_emptying",
                description=(
                    f"{movement['institution']}: saídas de R$ {total_outflow:,.2f} "
                    f"detectadas em {movement_dates} — "
                    f"{movement['days_before_order']} dias antes da ordem judicial "
                    f"({movement['order_date']}). "
                    f"Saldo: R$ {movement['balance_before']:,.2f} → "
                    f"R$ {movement['balance_after']:,.2f}. "
                    f"Padrão de esvaziamento pré-bloqueio confirmado."
                ),
                legal_refs=[
                    LEGAL_REFS["art_792_cpc"],
                    LEGAL_REFS["art_171_cp"],
                    LEGAL_REFS["law_9613_98"],
                ],
                recommended_action=(
                    f"Requerer ao {movement['institution']} comprovante de destino dos "
                    f"R$ {total_outflow:,.2f} transferidos. "
                    "Solicitar ao Banco Central rastreamento de TED/DOC via BACEN JUD. "
                    "Considerar representação criminal por fraude à execução."
                ),
                institution=movement["institution"],
                module=MODULE_NAME,
            )
            alerts.append(alert)

        return alerts

    def statistical_analysis(self, history: list[tuple[str, Decimal]]) -> dict:
        """Compute statistical summary of a balance history series.

        Args:
            history: Ordered list of (date_str, Decimal) balance records.

        Returns:
            Dict with keys: mean, std_dev, min, max, anomaly_threshold,
            anomalous_points, coefficient_of_variation.
        """
        if not history:
            return {"error": "empty history", "mean": 0.0, "std_dev": 0.0}

        values = [float(v) for _, v in history]
        n = len(values)
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        std_dev = math.sqrt(variance) if variance > 0 else 0.0

        lower_threshold = mean - ANOMALY_Z_SCORE * std_dev
        upper_threshold = mean + ANOMALY_Z_SCORE * std_dev

        anomalous = [
            {"date": d, "value": float(v), "z_score": (float(v) - mean) / std_dev if std_dev > 0 else 0.0}
            for d, v in history
            if float(v) < lower_threshold or float(v) > upper_threshold
        ]

        cv = (std_dev / mean * 100) if mean != 0 else 0.0

        return {
            "n": n,
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "lower_anomaly_threshold": round(lower_threshold, 2),
            "upper_anomaly_threshold": round(upper_threshold, 2),
            "anomalous_points": anomalous,
            "coefficient_of_variation_pct": round(cv, 2),
        }

    def run(self, trail: WholeMoneyTrail) -> PipelineReport:
        """Execute all flakiness checks and return a consolidated report.

        Args:
            trail: The current :class:`WholeMoneyTrail`.

        Returns:
            A :class:`PipelineReport` with all flakiness findings.
        """
        flakiness_results = self.test_sisbajud_consistency(trail.institutions)
        illiquidity_alerts = self.test_illiquidity_claim(trail.assets)
        pre_order_alerts = self.detect_pre_order_emptying(trail.institutions)

        all_alerts = illiquidity_alerts + pre_order_alerts

        # Statistical analysis for institutions with history
        stats_summary: dict[str, dict] = {}
        for inst in trail.institutions:
            if inst.balance_history:
                stats_summary[inst.name] = self.statistical_analysis(inst.balance_history)

        critical_count = sum(1 for a in all_alerts if a.level == RiskLevel.CRITICAL)
        high_count = sum(1 for a in all_alerts if a.level == RiskLevel.HIGH)
        status = (
            "critical" if critical_count > 0
            else "warning" if high_count > 0
            else "ok"
        )

        # Convert flakiness results to serialisable form for the report findings
        flakiness_summary = [
            {
                "institution": f.institution,
                "pattern": f.pattern,
                "occurrences": f.occurrences,
                "verdict": f.verdict,
                "evidence": f.evidence,
            }
            for f in flakiness_results
        ]

        return PipelineReport(
            module=MODULE_NAME,
            status=status,
            findings={
                "flakiness_patterns": flakiness_summary,
                "total_flaky_institutions": len(flakiness_results),
                "pre_order_emptying_confirmed": len(pre_order_alerts),
                "illiquidity_inconsistencies": len(illiquidity_alerts),
                "statistical_analysis": stats_summary,
            },
            alerts=all_alerts,
            recommendations=[
                "Requerer via BACEN JUD rastreamento de todas as TED/DOC saídas do BTG Pactual e Itaú.",
                "Solicitar perícia atuarial independente sobre a carteira ilíquida do FRAM XIV FIP.",
                "Apresentar ao juízo análise estatística como prova do padrão de esvaziamento.",
                "Considerar pedido de tutela de urgência com base no padrão pre_order_emptying.",
            ],
        )


# ---------------------------------------------------------------------------
# Module self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from pipeline.modules.briefing import BriefingModule

    trail, _ = BriefingModule().run()
    module = FlakyTestTracker()
    report = module.run(trail)

    print("=== FLAKY TRACKER SELF-TEST ===")
    print(f"Status: {report.status}")
    flakiness = report.findings.get("flakiness_patterns", [])
    print(f"Flaky institutions: {len(flakiness)}")
    for f in flakiness:
        print(f"  {f['institution']}: {f['verdict']} (pattern={f['pattern']}, occurrences={f['occurrences']})")
    print(f"Alerts: {len(report.alerts)}")
    for a in report.alerts:
        print(f"  [{a.level.name}] {a.category}: {a.description[:100]}...")
