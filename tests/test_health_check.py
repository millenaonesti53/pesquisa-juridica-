"""Tests for the System Health Check module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from decimal import Decimal
import pytest
from pipeline.modules.briefing import BriefingModule
from pipeline.modules.health_check import SystemHealthCheck
from pipeline.models import RiskLevel, SisbajudCode


def _get_trail():
    module = BriefingModule()
    trail, _ = module.run()
    return trail


def test_check_api_status_returns_dict():
    check = SystemHealthCheck()
    status = check.check_api_status()
    assert isinstance(status, dict)
    assert "CVM_API" in status
    assert "SISBAJUD_API" in status


def test_check_api_status_has_offline():
    check = SystemHealthCheck()
    status = check.check_api_status()
    offline = [k for k, v in status.items() if v == "offline"]
    assert len(offline) >= 2  # FRAM and OSLO integrators


def test_detect_non_responses_flags_code98():
    check = SystemHealthCheck()
    trail = _get_trail()
    alerts = check.detect_non_responses(trail.institutions)
    non_resp = [a for a in alerts if a.category == "sisbajud_non_response"]
    assert len(non_resp) >= 2
    names = {a.institution for a in non_resp}
    assert "FRAM Capital" in names
    assert "OSLO Gestora" in names


def test_detect_balance_anomalies_flags_itau():
    check = SystemHealthCheck()
    trail = _get_trail()
    alerts = check.detect_balance_anomalies(trail.institutions)
    institutions = {a.institution for a in alerts}
    assert "Itaú Unibanco" in institutions


def test_detect_balance_anomalies_flags_btg():
    check = SystemHealthCheck()
    trail = _get_trail()
    alerts = check.detect_balance_anomalies(trail.institutions)
    institutions = {a.institution for a in alerts}
    assert "BTG Pactual" in institutions


def test_run_returns_critical_status():
    check = SystemHealthCheck()
    trail = _get_trail()
    report = check.run(trail)
    assert report.status == "critical"
    assert report.module == "SYSTEM_HEALTH_CHECK"


def test_run_findings_contain_non_responses():
    check = SystemHealthCheck()
    trail = _get_trail()
    report = check.run(trail)
    assert report.findings["non_responses"] >= 2
