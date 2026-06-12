"""
Tests for pipeline/modules/briefing.py

Covers:
    - load_money_trail returns all 7 known assets
    - FRAM XIV FIP has correct value and Code 98
    - Itaú account has EMPTIED status
    - Bonifácio FIP has is_post_litigation=True
    - generate_alerts produces CRITICAL alerts for FRAM/OSLO non-response
    - generate_alerts produces CRITICAL alert for Itaú tactical emptying
    - generate_alerts produces CRITICAL alert for Bonifácio post-litigation
    - BTG zero-balance after movement alert is generated
    - generate_daily_report returns status 'critical' when there are critical alerts
    - update_institution_status upgrades risk levels correctly
    - compute_totals gives correct total_tracked
"""

from __future__ import annotations

import pytest
from decimal import Decimal

from pipeline.models import (
    AssetStatus,
    RiskLevel,
    SisbajudCode,
    WholeMoneyTrail,
)
from pipeline.modules.briefing import BriefingModule


@pytest.fixture
def module() -> BriefingModule:
    return BriefingModule()


@pytest.fixture
def trail(module: BriefingModule) -> WholeMoneyTrail:
    return module.load_money_trail("2024-01-15")


# ---------------------------------------------------------------------------
# load_money_trail
# ---------------------------------------------------------------------------


def test_load_money_trail_returns_7_assets(trail):
    assert len(trail.assets) == 7


def test_load_money_trail_has_correct_date(trail):
    assert trail.date == "2024-01-15"


def test_load_money_trail_fram_fip_value(trail):
    fram = next(a for a in trail.assets if "FRAM" in a.name)
    assert fram.value_brl == Decimal("3877255.47")
    assert fram.sisbajud_code == SisbajudCode.CODE_98
    assert fram.risk_level == RiskLevel.CRITICAL


def test_load_money_trail_lig_itau(trail):
    lig = next(a for a in trail.assets if "LIG" in a.name)
    assert lig.value_brl == Decimal("1250000.00")
    assert lig.institution == "Itaú Unibanco"


def test_load_money_trail_cdb_btg(trail):
    cdb = next(a for a in trail.assets if "CDB" in a.name)
    assert cdb.value_brl == Decimal("650758.60")
    assert cdb.institution == "BTG Pactual"


def test_load_money_trail_itau_account_emptied(trail):
    conta = next(a for a in trail.assets if a.asset_type == "conta_corrente")
    assert conta.status == AssetStatus.EMPTIED
    assert conta.value_brl == Decimal("5491.00")


def test_load_money_trail_bonifacio_post_litigation(trail):
    bonifacio = next(a for a in trail.assets if "Bonifácio" in a.name or "Bonifacio" in a.name)
    assert bonifacio.is_post_litigation is True
    # Created after 2022-03-15
    from datetime import date
    creation = date.fromisoformat(bonifacio.creation_date)
    litigation_start = date.fromisoformat("2022-03-15")
    assert creation > litigation_start


def test_load_money_trail_oslo_unresponsive(trail):
    oslo = next(a for a in trail.assets if "OSLO" in a.name)
    assert oslo.sisbajud_code == SisbajudCode.CODE_98
    assert oslo.status in {AssetStatus.UNRESPONSIVE, AssetStatus.SUSPICIOUS}


def test_load_money_trail_compute_totals_positive(trail):
    # Total tracked should be sum of all asset values
    expected = sum(a.value_brl for a in trail.assets)
    assert trail.total_tracked == expected


def test_load_money_trail_institutions_count(trail):
    assert len(trail.institutions) >= 4  # BTG, Itaú, FRAM, OSLO minimum


# ---------------------------------------------------------------------------
# update_institution_status
# ---------------------------------------------------------------------------


def test_update_institution_status_upgrades_to_critical(module, trail):
    institutions = module.update_institution_status(trail)
    # FRAM Capital should be CRITICAL (asset is CRITICAL)
    fram_inst = next((i for i in institutions if "FRAM" in i.name), None)
    if fram_inst:
        assert fram_inst.risk_level == RiskLevel.CRITICAL


# ---------------------------------------------------------------------------
# generate_alerts
# ---------------------------------------------------------------------------


def test_generate_alerts_produces_non_response_for_fram(module, trail):
    alerts = module.generate_alerts(trail)
    non_response = [
        a for a in alerts
        if a.category == "non_response" and "FRAM" in (a.institution or "")
    ]
    assert len(non_response) >= 1
    assert all(a.level == RiskLevel.CRITICAL for a in non_response)


def test_generate_alerts_produces_non_response_for_oslo(module, trail):
    alerts = module.generate_alerts(trail)
    non_response = [
        a for a in alerts
        if a.category == "non_response" and "OSLO" in (a.institution or "")
    ]
    assert len(non_response) >= 1


def test_generate_alerts_produces_tactical_emptying(module, trail):
    alerts = module.generate_alerts(trail)
    emptying = [a for a in alerts if a.category == "tactical_emptying"]
    assert len(emptying) >= 1
    assert any("Itaú" in (a.institution or "") for a in emptying)


def test_generate_alerts_produces_post_litigation_alert(module, trail):
    alerts = module.generate_alerts(trail)
    post_lit = [a for a in alerts if a.category == "post_litigation_creation"]
    assert len(post_lit) >= 1
    assert any(a.level == RiskLevel.CRITICAL for a in post_lit)


def test_generate_alerts_produces_btg_zero_balance_alert(module, trail):
    alerts = module.generate_alerts(trail)
    btg_alerts = [
        a for a in alerts
        if "BTG" in (a.institution or "") and a.level in {RiskLevel.CRITICAL, RiskLevel.HIGH}
    ]
    assert len(btg_alerts) >= 1


def test_generate_alerts_attaches_to_trail(module, trail):
    alerts = module.generate_alerts(trail)
    # Alerts should be attached to trail.alerts
    assert len(trail.alerts) > 0


def test_generate_alerts_all_have_legal_refs(module, trail):
    alerts = module.generate_alerts(trail)
    for alert in alerts:
        assert len(alert.legal_refs) > 0, f"Alert {alert.category} has no legal refs"


def test_generate_alerts_all_have_recommended_action(module, trail):
    alerts = module.generate_alerts(trail)
    for alert in alerts:
        assert alert.recommended_action, f"Alert {alert.category} missing recommended_action"


# ---------------------------------------------------------------------------
# generate_daily_report
# ---------------------------------------------------------------------------


def test_generate_daily_report_status_critical(module, trail):
    alerts = module.generate_alerts(trail)
    report = module.generate_daily_report(trail, alerts)
    assert report.status == "critical"


def test_generate_daily_report_has_findings(module, trail):
    alerts = module.generate_alerts(trail)
    report = module.generate_daily_report(trail, alerts)
    assert "investigation_date" in report.findings
    assert report.findings["investigation_date"] == "2024-01-15"


def test_generate_daily_report_non_responders_in_findings(module, trail):
    module.update_institution_status(trail)
    alerts = module.generate_alerts(trail)
    report = module.generate_daily_report(trail, alerts)
    non_responders = report.findings.get("non_responsive_institutions") or report.findings.get("non_responders", [])
    assert len(non_responders) >= 2  # FRAM and OSLO


def test_generate_daily_report_has_recommendations(module, trail):
    alerts = module.generate_alerts(trail)
    report = module.generate_daily_report(trail, alerts)
    assert len(report.recommendations) >= 3


# ---------------------------------------------------------------------------
# run() integration
# ---------------------------------------------------------------------------


def test_run_integration(module):
    trail, report = module.run("2024-01-15")
    assert trail is not None
    assert report is not None
    assert report.status in {"ok", "warning", "critical"}
    assert len(trail.assets) == 7
