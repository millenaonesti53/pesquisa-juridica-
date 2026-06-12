"""Tests for the Flaky Tracker module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from decimal import Decimal
import pytest
from pipeline.modules.briefing import BriefingModule
from pipeline.modules.flaky_tracker import FlakyTestTracker
from pipeline.models import Institution, RiskLevel, SisbajudCode


def _get_trail():
    module = BriefingModule()
    trail, _ = module.run()
    return trail


def test_statistical_analysis_basic():
    tracker = FlakyTestTracker()
    history = [
        ("2024-01-01", Decimal("100.00")),
        ("2024-02-01", Decimal("200.00")),
        ("2024-03-01", Decimal("150.00")),
    ]
    result = tracker.statistical_analysis(history)
    assert abs(result["mean"] - 150.0) < 0.01
    assert result["std_dev"] >= 0
    # key may be named lower_anomaly_threshold or anomaly_threshold depending on module version
    assert any(k for k in result if "anomaly" in k and "threshold" in k)


def test_statistical_analysis_empty():
    tracker = FlakyTestTracker()
    result = tracker.statistical_analysis([])
    assert result["mean"] == 0.0


def test_test_sisbajud_consistency_btg():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    results = tracker.test_sisbajud_consistency(trail.institutions)
    institutions = {r.institution for r in results}
    assert "BTG Pactual" in institutions


def test_test_sisbajud_consistency_non_responsive():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    results = tracker.test_sisbajud_consistency(trail.institutions)
    non_compliant = [r for r in results if "NON" in r.verdict.upper() or "SILENCE" in r.pattern.upper()]
    assert len(non_compliant) >= 1


def test_detect_pre_order_emptying_itau():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    alerts = tracker.detect_pre_order_emptying(trail.institutions)
    institutions = {a.institution for a in alerts}
    assert "Itaú Unibanco" in institutions


def test_detect_pre_order_emptying_is_critical():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    alerts = tracker.detect_pre_order_emptying(trail.institutions)
    for a in alerts:
        assert a.level == RiskLevel.CRITICAL


def test_run_returns_critical():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    report = tracker.run(trail)
    assert report.status == "critical"
    assert report.module == "FLAKY_TRACKER"


def test_illiquidity_claim_produces_alerts():
    tracker = FlakyTestTracker()
    trail = _get_trail()
    alerts = tracker.test_illiquidity_claim(trail.assets)
    assert len(alerts) >= 1
    categories = {a.category for a in alerts}
    # Should flag unverifiable illiquidity for FRAM/OSLO
    assert any("illiquid" in c for c in categories)
