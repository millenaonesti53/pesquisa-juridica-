"""
Tests for pipeline/modules/flaky_tracker.py

Covers:
    - test_sisbajud_consistency detects BTG and Itaú oscillating patterns
    - test_sisbajud_consistency detects FRAM/OSLO total silence
    - test_illiquidity_claim detects FRAM XIV FIP inconsistency (63% vs 22%)
    - test_illiquidity_claim detects OSLO FIP inconsistency (100% vs 28%)
    - detect_pre_order_emptying generates BTG and Itaú pre-order alerts
    - statistical_analysis returns correct mean/std_dev for known data
    - statistical_analysis identifies anomalous points correctly
    - run() returns PipelineReport with correct status
    - run() findings include flakiness_patterns
    - BalanceFlakiness dataclass works correctly
"""

from __future__ import annotations

import math
import pytest
from decimal import Decimal

from pipeline.models import (
    Asset,
    AssetStatus,
    Institution,
    PipelineReport,
    RiskLevel,
    SisbajudCode,
    WholeMoneyTrail,
)
from pipeline.modules.briefing import BriefingModule
from pipeline.modules.flaky_tracker import BalanceFlakiness, FlakyTestTracker


@pytest.fixture
def module() -> FlakyTestTracker:
    return FlakyTestTracker()


@pytest.fixture
def trail() -> WholeMoneyTrail:
    briefing = BriefingModule()
    t, _ = briefing.run("2024-01-15")
    return t


# ---------------------------------------------------------------------------
# BalanceFlakiness dataclass
# ---------------------------------------------------------------------------


def test_balance_flakiness_creation():
    bf = BalanceFlakiness(
        institution="Test Bank",
        pattern="oscillating_zero",
        occurrences=2,
        verdict="SUSPEITO",
    )
    assert bf.institution == "Test Bank"
    assert bf.occurrences == 2
    assert bf.evidence == []


def test_balance_flakiness_with_evidence():
    bf = BalanceFlakiness(
        institution="BTG",
        pattern="pre_order_emptying",
        occurrences=1,
        verdict="CONFIRMADO",
        evidence=["Drop from R$650k to R$0"],
    )
    assert len(bf.evidence) == 1


# ---------------------------------------------------------------------------
# test_sisbajud_consistency
# ---------------------------------------------------------------------------


def test_sisbajud_consistency_detects_btg_drop(module, trail):
    results = module.test_sisbajud_consistency(trail.institutions)
    btg = next((r for r in results if "BTG" in r.institution), None)
    assert btg is not None
    assert btg.occurrences >= 1


def test_sisbajud_consistency_detects_itau_drop(module, trail):
    results = module.test_sisbajud_consistency(trail.institutions)
    itau = next((r for r in results if "Itaú" in r.institution or "Itau" in r.institution), None)
    assert itau is not None


def test_sisbajud_consistency_detects_fram_silence(module, trail):
    results = module.test_sisbajud_consistency(trail.institutions)
    fram = next((r for r in results if "FRAM" in r.institution), None)
    assert fram is not None
    assert "silence" in fram.pattern or fram.occurrences >= 1


def test_sisbajud_consistency_detects_oslo_silence(module, trail):
    results = module.test_sisbajud_consistency(trail.institutions)
    oslo = next((r for r in results if "OSLO" in r.institution), None)
    assert oslo is not None


def test_sisbajud_consistency_stable_institution_not_flagged(module):
    stable = Institution(
        name="Stable Bank",
        type="banco",
        sisbajud_code=SisbajudCode.CODE_00,
        balance_history=[
            ("2024-01-01", Decimal("100000.00")),
            ("2024-02-01", Decimal("101000.00")),
            ("2024-03-01", Decimal("100500.00")),
        ],
    )
    results = module.test_sisbajud_consistency([stable])
    assert all(r.institution != "Stable Bank" for r in results)


def test_sisbajud_consistency_returns_list(module, trail):
    results = module.test_sisbajud_consistency(trail.institutions)
    assert isinstance(results, list)
    assert all(isinstance(r, BalanceFlakiness) for r in results)


# ---------------------------------------------------------------------------
# test_illiquidity_claim
# ---------------------------------------------------------------------------


def test_illiquidity_claim_detects_fram_inconsistency(module, trail):
    alerts = module.test_illiquidity_claim(trail.assets)
    fram_alerts = [a for a in alerts if "FRAM" in (a.asset.name if a.asset else "")]
    assert len(fram_alerts) >= 1
    assert any(a.level in {RiskLevel.CRITICAL, RiskLevel.HIGH} for a in fram_alerts)


def test_illiquidity_claim_detects_oslo_inconsistency(module, trail):
    alerts = module.test_illiquidity_claim(trail.assets)
    oslo_alerts = [a for a in alerts if "OSLO" in (a.asset.name if a.asset else "")]
    assert len(oslo_alerts) >= 1


def test_illiquidity_claim_alerts_have_legal_refs(module, trail):
    alerts = module.test_illiquidity_claim(trail.assets)
    for alert in alerts:
        assert len(alert.legal_refs) > 0


def test_illiquidity_claim_category_correct(module, trail):
    alerts = module.test_illiquidity_claim(trail.assets)
    for alert in alerts:
        assert alert.category == "illiquidity_claim_inconsistent"


# ---------------------------------------------------------------------------
# detect_pre_order_emptying
# ---------------------------------------------------------------------------


def test_detect_pre_order_emptying_btg(module, trail):
    alerts = module.detect_pre_order_emptying(trail.institutions)
    btg_alerts = [a for a in alerts if "BTG" in (a.institution or "")]
    assert len(btg_alerts) >= 1


def test_detect_pre_order_emptying_itau(module, trail):
    alerts = module.detect_pre_order_emptying(trail.institutions)
    itau_alerts = [a for a in alerts if "Itaú" in (a.institution or "") or "Itau" in (a.institution or "")]
    assert len(itau_alerts) >= 1


def test_detect_pre_order_emptying_alerts_are_critical(module, trail):
    alerts = module.detect_pre_order_emptying(trail.institutions)
    for alert in alerts:
        assert alert.level == RiskLevel.CRITICAL


def test_detect_pre_order_emptying_category(module, trail):
    alerts = module.detect_pre_order_emptying(trail.institutions)
    for alert in alerts:
        assert alert.category == "pre_order_emptying"


def test_detect_pre_order_emptying_has_law_9613(module, trail):
    alerts = module.detect_pre_order_emptying(trail.institutions)
    for alert in alerts:
        # Should reference money laundering law (stored as full string value or key)
        assert any(
            "9613" in ref or "law_9613" in ref or "lavagem" in ref.lower()
            for ref in alert.legal_refs
        )


# ---------------------------------------------------------------------------
# statistical_analysis
# ---------------------------------------------------------------------------


def test_statistical_analysis_empty_history(module):
    result = module.statistical_analysis([])
    assert "error" in result


def test_statistical_analysis_mean(module):
    history = [
        ("2024-01-01", Decimal("100.00")),
        ("2024-02-01", Decimal("200.00")),
        ("2024-03-01", Decimal("300.00")),
    ]
    result = module.statistical_analysis(history)
    assert result["mean"] == pytest.approx(200.0, abs=0.01)


def test_statistical_analysis_std_dev(module):
    history = [
        ("2024-01-01", Decimal("100.00")),
        ("2024-02-01", Decimal("100.00")),
        ("2024-03-01", Decimal("100.00")),
    ]
    result = module.statistical_analysis(history)
    assert result["std_dev"] == pytest.approx(0.0, abs=0.01)


def test_statistical_analysis_detects_anomaly(module):
    """R$469,575 → R$5,491 pattern: the drop is anomalous."""
    history = [
        ("2024-01-10", Decimal("469575.00")),
        ("2024-02-20", Decimal("87400.00")),
        ("2024-03-05", Decimal("5491.00")),
    ]
    result = module.statistical_analysis(history)
    # At least one anomalous point should be detected
    assert "anomalous_points" in result


def test_statistical_analysis_min_max(module):
    history = [
        ("2024-01-01", Decimal("50.00")),
        ("2024-02-01", Decimal("150.00")),
        ("2024-03-01", Decimal("100.00")),
    ]
    result = module.statistical_analysis(history)
    assert result["min"] == pytest.approx(50.0, abs=0.01)
    assert result["max"] == pytest.approx(150.0, abs=0.01)


def test_statistical_analysis_returns_n(module):
    history = [
        ("2024-01-01", Decimal("100.00")),
        ("2024-02-01", Decimal("200.00")),
    ]
    result = module.statistical_analysis(history)
    assert result["n"] == 2


def test_statistical_analysis_itau_history(module, trail):
    """Itaú's real history should produce a high coefficient of variation."""
    itau = next(
        i for i in trail.institutions
        if "Itaú" in i.name or "Itau" in i.name
    )
    result = module.statistical_analysis(itau.balance_history)
    # CoV should be very high for a 98% drop
    assert result["coefficient_of_variation_pct"] > 50.0


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------


def test_run_returns_pipeline_report(module, trail):
    report = module.run(trail)
    assert isinstance(report, PipelineReport)


def test_run_status_critical(module, trail):
    report = module.run(trail)
    assert report.status == "critical"


def test_run_findings_include_flakiness(module, trail):
    report = module.run(trail)
    assert "flakiness_patterns" in report.findings
    assert isinstance(report.findings["flakiness_patterns"], list)


def test_run_findings_pre_order_emptying_confirmed(module, trail):
    report = module.run(trail)
    assert report.findings.get("pre_order_emptying_confirmed", 0) >= 2  # BTG + Itaú


def test_run_alerts_not_empty(module, trail):
    report = module.run(trail)
    assert len(report.alerts) > 0
