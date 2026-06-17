"""
Tests for pipeline/models.py

Covers:
    - SisbajudCode enum values
    - RiskLevel ordering operators
    - AssetStatus enum values
    - Asset dataclass creation and __str__
    - Institution dataclass: latest_balance, previous_balance
    - Alert dataclass and __str__
    - WholeMoneyTrail.compute_totals()
    - PipelineReport.worst_risk_level() and alert_count_by_level()
"""

from __future__ import annotations

import pytest
from decimal import Decimal
from datetime import datetime

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


# ---------------------------------------------------------------------------
# SisbajudCode
# ---------------------------------------------------------------------------


def test_sisbajud_code_values():
    assert SisbajudCode.CODE_00.value == "00"
    assert SisbajudCode.CODE_13.value == "13"
    assert SisbajudCode.CODE_98.value == "98"


def test_sisbajud_code_members():
    codes = {c.value for c in SisbajudCode}
    assert codes == {"00", "13", "98"}


# ---------------------------------------------------------------------------
# RiskLevel
# ---------------------------------------------------------------------------


def test_risk_level_ordering():
    assert RiskLevel.LOW < RiskLevel.MEDIUM
    assert RiskLevel.MEDIUM < RiskLevel.HIGH
    assert RiskLevel.HIGH < RiskLevel.CRITICAL


def test_risk_level_le_ge():
    assert RiskLevel.LOW <= RiskLevel.LOW
    assert RiskLevel.CRITICAL >= RiskLevel.HIGH


def test_risk_level_max():
    levels = [RiskLevel.LOW, RiskLevel.CRITICAL, RiskLevel.MEDIUM]
    assert max(levels) == RiskLevel.CRITICAL


def test_risk_level_sorting():
    levels = [RiskLevel.HIGH, RiskLevel.LOW, RiskLevel.CRITICAL, RiskLevel.MEDIUM]
    assert sorted(levels) == [
        RiskLevel.LOW,
        RiskLevel.MEDIUM,
        RiskLevel.HIGH,
        RiskLevel.CRITICAL,
    ]


# ---------------------------------------------------------------------------
# Asset
# ---------------------------------------------------------------------------


def test_asset_creation_defaults():
    asset = Asset(
        name="Test Asset",
        institution="Test Bank",
        value_brl=Decimal("100.00"),
        asset_type="CDB",
    )
    assert asset.status == AssetStatus.ACTIVE
    assert asset.risk_level == RiskLevel.MEDIUM
    assert asset.sisbajud_code is None
    assert asset.is_post_litigation is False
    assert asset.id is not None


def test_asset_str():
    asset = Asset(
        name="CDB BTG",
        institution="BTG Pactual",
        value_brl=Decimal("650758.60"),
        asset_type="CDB",
        status=AssetStatus.SUSPICIOUS,
    )
    s = str(asset)
    assert "CDB BTG" in s
    assert "BTG Pactual" in s
    assert "suspicious" in s


def test_asset_fram_fip_values():
    """Test that the FRAM XIV FIP canonical values are representable."""
    asset = Asset(
        name="FRAM XIV FIP",
        institution="FRAM Capital",
        value_brl=Decimal("3877255.47"),
        asset_type="FIP",
        status=AssetStatus.SUSPICIOUS,
        sisbajud_code=SisbajudCode.CODE_98,
        risk_level=RiskLevel.CRITICAL,
    )
    assert asset.value_brl == Decimal("3877255.47")
    assert asset.sisbajud_code == SisbajudCode.CODE_98
    assert asset.risk_level == RiskLevel.CRITICAL


def test_asset_post_litigation_flag():
    asset = Asset(
        name="Bonifácio FIP",
        institution="Bonifácio Gestora",
        value_brl=Decimal("0.00"),
        asset_type="FIP",
        is_post_litigation=True,
        creation_date="2022-09-10",
    )
    assert asset.is_post_litigation is True
    assert asset.creation_date == "2022-09-10"


def test_asset_unique_ids():
    a1 = Asset(name="A", institution="B", value_brl=Decimal("1"), asset_type="CDB")
    a2 = Asset(name="A", institution="B", value_brl=Decimal("1"), asset_type="CDB")
    assert a1.id != a2.id


# ---------------------------------------------------------------------------
# Institution
# ---------------------------------------------------------------------------


def test_institution_latest_balance():
    inst = Institution(
        name="BTG Pactual",
        type="banco",
        balance_history=[
            ("2024-01-01", Decimal("500000.00")),
            ("2024-02-01", Decimal("0.00")),
        ],
    )
    assert inst.latest_balance() == Decimal("0.00")


def test_institution_previous_balance():
    inst = Institution(
        name="Itaú",
        type="banco",
        balance_history=[
            ("2024-01-01", Decimal("469575.00")),
            ("2024-02-01", Decimal("5491.00")),
        ],
    )
    assert inst.previous_balance() == Decimal("469575.00")


def test_institution_no_history():
    inst = Institution(name="FRAM Capital", type="gestora_fip")
    assert inst.latest_balance() is None
    assert inst.previous_balance() is None


def test_institution_single_history():
    inst = Institution(
        name="X",
        type="banco",
        balance_history=[("2024-01-01", Decimal("1000.00"))],
    )
    assert inst.latest_balance() == Decimal("1000.00")
    assert inst.previous_balance() is None


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------


def test_alert_creation():
    alert = Alert(
        level=RiskLevel.CRITICAL,
        category="tactical_emptying",
        description="Test description",
        institution="Itaú Unibanco",
    )
    assert alert.level == RiskLevel.CRITICAL
    assert alert.id is not None
    assert alert.timestamp is not None


def test_alert_str():
    alert = Alert(
        level=RiskLevel.HIGH,
        category="non_response",
        description="FRAM Capital did not respond",
    )
    s = str(alert)
    assert "HIGH" in s
    assert "non_response" in s


def test_alert_unique_ids():
    a1 = Alert(level=RiskLevel.LOW, category="test", description="same")
    a2 = Alert(level=RiskLevel.LOW, category="test", description="same")
    assert a1.id != a2.id


# ---------------------------------------------------------------------------
# WholeMoneyTrail
# ---------------------------------------------------------------------------


def _make_trail() -> WholeMoneyTrail:
    assets = [
        Asset(
            name="FRAM XIV FIP",
            institution="FRAM Capital",
            value_brl=Decimal("3877255.47"),
            asset_type="FIP",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_98,
            risk_level=RiskLevel.CRITICAL,
        ),
        Asset(
            name="CDB BTG",
            institution="BTG Pactual",
            value_brl=Decimal("650758.60"),
            asset_type="CDB",
            status=AssetStatus.SUSPICIOUS,
            sisbajud_code=SisbajudCode.CODE_13,
            risk_level=RiskLevel.HIGH,
        ),
        Asset(
            name="Conta Corrente Itaú",
            institution="Itaú Unibanco",
            value_brl=Decimal("5491.00"),
            asset_type="conta_corrente",
            status=AssetStatus.EMPTIED,
            sisbajud_code=SisbajudCode.CODE_13,
            risk_level=RiskLevel.CRITICAL,
        ),
    ]
    trail = WholeMoneyTrail(date="2024-01-15", assets=assets)
    return trail


def test_money_trail_compute_totals():
    trail = _make_trail()
    trail.compute_totals()

    expected_total = Decimal("3877255.47") + Decimal("650758.60") + Decimal("5491.00")
    assert trail.total_tracked == expected_total


def test_money_trail_total_blocked_zero():
    """No assets have Code 00, so total_blocked should be zero."""
    trail = _make_trail()
    trail.compute_totals()
    assert trail.total_blocked == Decimal("0.00")


def test_money_trail_total_evaded():
    """EMPTIED assets contribute to total_evaded."""
    trail = _make_trail()
    trail.compute_totals()
    # Only the Conta Corrente Itaú (EMPTIED) contributes
    assert trail.total_evaded == Decimal("5491.00")


def test_money_trail_unresponsive_evaded():
    """UNRESPONSIVE assets also contribute to total_evaded."""
    asset = Asset(
        name="OSLO FIP",
        institution="OSLO Capital",
        value_brl=Decimal("0.00"),
        asset_type="FIP",
        status=AssetStatus.UNRESPONSIVE,
        sisbajud_code=SisbajudCode.CODE_98,
        risk_level=RiskLevel.CRITICAL,
    )
    trail = WholeMoneyTrail(date="2024-01-15", assets=[asset])
    trail.compute_totals()
    # OSLO FIP has value 0, but is UNRESPONSIVE
    assert trail.total_evaded == Decimal("0.00")


# ---------------------------------------------------------------------------
# PipelineReport
# ---------------------------------------------------------------------------


def test_pipeline_report_worst_risk_no_alerts():
    report = PipelineReport(module="test", status="ok")
    assert report.worst_risk_level() is None


def test_pipeline_report_worst_risk_level():
    alerts = [
        Alert(level=RiskLevel.HIGH, category="a", description="x"),
        Alert(level=RiskLevel.CRITICAL, category="b", description="y"),
        Alert(level=RiskLevel.LOW, category="c", description="z"),
    ]
    report = PipelineReport(module="test", status="critical", alerts=alerts)
    assert report.worst_risk_level() == RiskLevel.CRITICAL


def test_pipeline_report_alert_count_by_level():
    alerts = [
        Alert(level=RiskLevel.CRITICAL, category="a", description="x"),
        Alert(level=RiskLevel.CRITICAL, category="b", description="y"),
        Alert(level=RiskLevel.HIGH, category="c", description="z"),
        Alert(level=RiskLevel.LOW, category="d", description="w"),
    ]
    report = PipelineReport(module="test", status="critical", alerts=alerts)
    counts = report.alert_count_by_level()
    assert counts["CRITICAL"] == 2
    assert counts["HIGH"] == 1
    assert counts["MEDIUM"] == 0
    assert counts["LOW"] == 1
