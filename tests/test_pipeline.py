"""Integration tests for the Corporate Cognitive Pipeline."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from decimal import Decimal

from pipeline.modules.briefing import BriefingModule
from pipeline.modules.health_check import HealthCheckModule
from pipeline.modules.dependency_check import DependencyCheckModule
from pipeline.modules.flaky_tracker import FlakyTrackerModule, FlakyPattern
from pipeline.core import CognitivePipeline
from models.assets import Asset, AssetType, RiskLevel


def test_briefing_generates_alerts():
    module = BriefingModule()
    report = module.run()
    assert len(report.assets) > 0
    assert report.total_identified > Decimal("0")
    assert len(report.critical_alerts) > 0


def test_briefing_detects_non_response():
    module = BriefingModule()
    report = module.run()
    non_response_alerts = [
        a for a in report.critical_alerts if "NAO_RESPOSTA" in a.alert_type.value
    ]
    assert len(non_response_alerts) > 0, "Should detect FRAM non-response"


def test_briefing_detects_tactical_drain():
    module = BriefingModule()
    report = module.run()
    drain_alerts = [
        a for a in report.critical_alerts if "ESVAZIAMENTO" in a.alert_type.value
    ]
    assert len(drain_alerts) > 0, "Should detect Itaú/BTG tactical drains"


def test_health_check_detects_non_responsive_institutions():
    module = HealthCheckModule()
    report = module.run()
    assert "FRAM" in report.non_responsive_institutions
    assert "OSLO" in report.non_responsive_institutions


def test_health_check_detects_tactical_drains():
    module = HealthCheckModule()
    report = module.run()
    assert len(report.tactical_drains) >= 2


def test_dependency_check_detects_post_litigation_fip():
    module = DependencyCheckModule()
    report = module.run()
    post_lit = report.critical_findings
    assert len(post_lit) > 0, "Should detect Bonifácio FIP created post-litigation"
    names = [f.fip_name for f in post_lit]
    assert any("Bonifácio" in n or "Classe J" in n or "FRAM" in n for n in names)


def test_dependency_check_detects_retroactive_class():
    module = DependencyCheckModule()
    report = module.run()
    assert len(report.retroactive_classes) > 0
    assert report.retroactive_classes[0]["class_name"] == "Classe J"


def test_flaky_tracker_detects_systematic_concealment():
    module = FlakyTrackerModule()
    report = module.run()
    assert report.systematic_concealment_detected, "Should detect systematic concealment pattern"


def test_flaky_tracker_btg_zero_balance_pattern():
    module = FlakyTrackerModule()
    report = module.run()
    btg_signals = [s for s in report.flaky_signals if s.institution == "BTG"]
    assert len(btg_signals) > 0
    assert btg_signals[0].pattern == FlakyPattern.ZERO_BALANCE_REPEAT


def test_flaky_tracker_itau_drain_pattern():
    module = FlakyTrackerModule()
    report = module.run()
    itau_signals = [s for s in report.flaky_signals if s.institution == "ITAU"]
    assert len(itau_signals) > 0
    assert itau_signals[0].pattern == FlakyPattern.TACTICAL_DRAIN


def test_full_pipeline_runs_successfully():
    pipeline = CognitivePipeline()
    result = pipeline.run()
    assert result.success
    assert result.duration_seconds >= 0
    assert result.has_critical_issues  # Investigation context has known critical issues
    assert result.pr_digest.total_recoverable > Decimal("0")


def test_full_pipeline_generates_clo_report():
    pipeline = CognitivePipeline()
    result = pipeline.run()
    clo = result.pr_digest.clo_report
    assert "RELATÓRIO CLO" in clo
    assert "FRAM" in clo or "BTG" in clo or "ITAU" in clo


def test_full_pipeline_generates_coaf_draft():
    pipeline = CognitivePipeline()
    result = pipeline.run()
    draft = result.pr_digest.coaf_mpf_draft
    assert "COAF" in draft
    assert "9.613" in draft  # Lei 9.613/98


def test_asset_drain_detection():
    asset = Asset(
        id="test_drain",
        institution="TEST",
        asset_type=AssetType.CONTA_CORRENTE,
        description="Test account",
        balance=Decimal("5000"),
        reference_date=datetime.now(),
        previous_balance=Decimal("500000"),
    )
    assert asset.is_suspect_drain, "Should detect >80% balance drop as suspect drain"


def test_asset_no_false_drain_on_small_accounts():
    asset = Asset(
        id="test_small",
        institution="TEST",
        asset_type=AssetType.CONTA_CORRENTE,
        description="Small account",
        balance=Decimal("800"),
        reference_date=datetime.now(),
        previous_balance=Decimal("1000"),
    )
    assert not asset.is_suspect_drain, "Should not flag normal 20% variation"
