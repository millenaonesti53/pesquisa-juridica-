"""
Tests for pipeline/modules/health_check.py

Covers:
    - check_api_status returns expected API keys
    - FRAM and OSLO integrators are 'offline'
    - detect_pl_inconsistencies: no false positives on exact match
    - detect_pl_inconsistencies: FRAM XIV FIP at exact CVM value → no alert
    - detect_balance_anomalies: Itaú drop triggers anomaly alert
    - detect_balance_anomalies: stable history → no alerts
    - detect_non_responses: Code 98 institutions trigger alerts
    - detect_non_responses: Code 13 institutions do NOT trigger non-response alerts
    - run() returns PipelineReport with status 'critical' for known data
    - run() report includes api_status in findings
"""

from __future__ import annotations

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
from pipeline.modules.health_check import SystemHealthCheck


@pytest.fixture
def module() -> SystemHealthCheck:
    return SystemHealthCheck()


@pytest.fixture
def trail() -> WholeMoneyTrail:
    briefing = BriefingModule()
    t, _ = briefing.run("2024-01-15")
    return t


# ---------------------------------------------------------------------------
# check_api_status
# ---------------------------------------------------------------------------


def test_check_api_status_returns_dict(module):
    status = module.check_api_status()
    assert isinstance(status, dict)
    assert len(status) > 0


def test_check_api_status_has_sisbajud_key(module):
    status = module.check_api_status()
    assert any("SISBAJUD" in k for k in status)


def test_check_api_status_fram_integrator_offline(module):
    status = module.check_api_status()
    assert any(
        ("FRAM" in k or "fram" in k.lower()) and v == "offline"
        for k, v in status.items()
    )


def test_check_api_status_oslo_integrator_offline(module):
    status = module.check_api_status()
    assert any(
        ("OSLO" in k or "oslo" in k.lower()) and v == "offline"
        for k, v in status.items()
    )


def test_check_api_status_btg_integrator_degraded(module):
    status = module.check_api_status()
    assert any(
        "BTG" in k.upper() and v == "degraded"
        for k, v in status.items()
    )


# ---------------------------------------------------------------------------
# detect_pl_inconsistencies
# ---------------------------------------------------------------------------


def test_detect_pl_inconsistencies_exact_match_no_alert(module):
    """FRAM XIV FIP at exact expected PL → no alert."""
    asset = Asset(
        name="FRAM XIV FIP",
        institution="FRAM Capital",
        value_brl=Decimal("3877255.47"),
        asset_type="FIP",
        status=AssetStatus.SUSPICIOUS,
        sisbajud_code=SisbajudCode.CODE_98,
        risk_level=RiskLevel.CRITICAL,
    )
    alerts = module.detect_pl_inconsistencies([asset])
    # At exact match, divergence = 0%, which is ≤ 5% → no alert expected
    assert all(a.category != "pl_inconsistency" for a in alerts)


def test_detect_pl_inconsistencies_large_divergence_triggers_alert(module):
    """If FRAM XIV FIP value were reported as only R$1M, divergence > 5% → alert."""
    asset = Asset(
        name="FRAM XIV FIP",
        institution="FRAM Capital",
        value_brl=Decimal("1000000.00"),  # Very different from 3.877M expected
        asset_type="FIP",
        status=AssetStatus.SUSPICIOUS,
        sisbajud_code=SisbajudCode.CODE_98,
        risk_level=RiskLevel.CRITICAL,
    )
    alerts = module.detect_pl_inconsistencies([asset])
    assert len(alerts) >= 1
    assert any(a.category == "pl_inconsistency" for a in alerts)


def test_detect_pl_inconsistencies_unknown_asset_no_alert(module):
    """Unknown asset name → no alert."""
    asset = Asset(
        name="Unknown FIP XYZ",
        institution="Unknown",
        value_brl=Decimal("999.00"),
        asset_type="FIP",
    )
    alerts = module.detect_pl_inconsistencies([asset])
    assert len(alerts) == 0


def test_detect_pl_inconsistencies_returns_list(module, trail):
    result = module.detect_pl_inconsistencies(trail.assets)
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# detect_balance_anomalies
# ---------------------------------------------------------------------------


def test_detect_balance_anomalies_itau_triggers(module, trail):
    """Itaú balance drop (469k → 5k) should trigger anomaly alert."""
    alerts = module.detect_balance_anomalies(trail.institutions)
    itau_anomalies = [
        a for a in alerts
        if "Itaú" in (a.institution or "") or "Itau" in (a.institution or "")
    ]
    assert len(itau_anomalies) >= 1


def test_detect_balance_anomalies_stable_no_alert(module):
    """Stable history (no big drops) should not trigger alert."""
    stable_inst = Institution(
        name="Stable Bank",
        type="banco",
        sisbajud_code=SisbajudCode.CODE_00,
        balance_history=[
            ("2024-01-01", Decimal("100000.00")),
            ("2024-02-01", Decimal("101000.00")),
            ("2024-03-01", Decimal("99500.00")),
            ("2024-04-01", Decimal("100200.00")),
        ],
    )
    alerts = module.detect_balance_anomalies([stable_inst])
    assert all(a.category != "balance_anomaly" for a in alerts)


def test_detect_balance_anomalies_no_history_no_alert(module):
    inst = Institution(name="OSLO Capital", type="gestora_fip")
    alerts = module.detect_balance_anomalies([inst])
    assert len(alerts) == 0


# ---------------------------------------------------------------------------
# detect_non_responses
# ---------------------------------------------------------------------------


def test_detect_non_responses_code_98_triggers(module, trail):
    alerts = module.detect_non_responses(trail.institutions)
    non_resp = [a for a in alerts if a.category == "sisbajud_non_response"]
    assert len(non_resp) >= 2  # FRAM and OSLO at minimum


def test_detect_non_responses_code_13_does_not_trigger(module):
    """Code 13 (zero balance) is NOT a non-response; should not trigger."""
    inst = Institution(
        name="BTG Pactual",
        type="banco",
        sisbajud_code=SisbajudCode.CODE_13,
    )
    alerts = module.detect_non_responses([inst])
    assert len(alerts) == 0


def test_detect_non_responses_code_00_does_not_trigger(module):
    inst = Institution(
        name="Clean Bank",
        type="banco",
        sisbajud_code=SisbajudCode.CODE_00,
    )
    alerts = module.detect_non_responses([inst])
    assert len(alerts) == 0


def test_detect_non_responses_alerts_are_critical(module, trail):
    alerts = module.detect_non_responses(trail.institutions)
    for alert in alerts:
        assert alert.level == RiskLevel.CRITICAL


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------


def test_run_returns_pipeline_report(module, trail):
    report = module.run(trail)
    assert isinstance(report, PipelineReport)


def test_run_status_is_critical(module, trail):
    report = module.run(trail)
    # With FRAM/OSLO offline and Itaú emptying, should be critical
    assert report.status == "critical"


def test_run_findings_include_api_status(module, trail):
    report = module.run(trail)
    assert "api_status" in report.findings


def test_run_findings_offline_apis_not_empty(module, trail):
    report = module.run(trail)
    assert len(report.findings.get("offline_apis", [])) > 0


def test_run_has_recommendations(module, trail):
    report = module.run(trail)
    assert len(report.recommendations) >= 2


def test_run_all_alerts_have_legal_refs(module, trail):
    report = module.run(trail)
    for alert in report.alerts:
        assert len(alert.legal_refs) > 0, f"Alert {alert.category} missing legal_refs"
