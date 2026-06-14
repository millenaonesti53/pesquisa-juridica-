"""
Módulo 2 — SYSTEM HEALTH CHECK
Monitora infraestrutura, detecta fraude e inconsistências patrimoniais.
Verifica inconsistências de PL, divergências IRPF × CVM, sinais de ocultação.
"""

from datetime import datetime
from typing import Optional

from pipeline.config import INSTITUTIONS_DATA, RISK_THRESHOLDS
from pipeline.models import (
    Alert, Asset, AssetStatus, Institution, InstitutionType,
    ModuleResult, RiskLevel,
)


_MOCK_HEALTH_STATUS = {
    "apis": {
        "CVM": {"status": "OK", "latency_ms": 142},
        "SISBAJUD": {"status": "DEGRADED", "latency_ms": 3800, "note": "Resposta lenta – possível sobrecarga"},
        "IRPF_RECEITA": {"status": "OK", "latency_ms": 210},
        "FATCA_CRS": {"status": "OK", "latency_ms": 180},
    },
    "integrators": {
        "FRAM": {"status": "OFFLINE", "last_seen": "2026-06-09T08:00:00"},
        "OSLO": {"status": "OFFLINE", "last_seen": "2026-06-08T14:30:00"},
        "BTG": {"status": "OK", "last_seen": "2026-06-14T06:00:00"},
        "ITAU": {"status": "OK", "last_seen": "2026-06-14T06:00:00"},
    },
}

_MOCK_PL_DIVERGENCES = [
    {
        "institution_id": "FRAM",
        "asset_id": "FRAM_XIV_FIP",
        "pl_cvm": 3_877_255.47,
        "pl_irpf": 4_100_000.00,
        "variance_pct": 5.4,
        "flag": "PL_CVM_MENOR_QUE_IRPF",
    },
    {
        "institution_id": "ITAU",
        "asset_id": "CC_ITAU",
        "pl_extrato": 469_575.00,
        "pl_sisbajud": 5_491.00,
        "variance_pct": 98.8,
        "flag": "ESVAZIAMENTO_CONFIRMADO",
    },
    {
        "institution_id": "BTG",
        "asset_id": "CDB_BTG",
        "pl_cvm": 650_758.60,
        "pl_sisbajud": 0.00,
        "variance_pct": 100.0,
        "flag": "SALDO_ZERO_SUSPEITO",
    },
]


def _check_api_health() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for api_name, info in _MOCK_HEALTH_STATUS["apis"].items():
        if info["status"] == "DEGRADED":
            alerts.append(Alert(
                level=RiskLevel.MEDIO,
                category="INFRAESTRUTURA",
                title=f"API degradada: {api_name}",
                description=f"{api_name} com latência alta ({info['latency_ms']}ms). {info.get('note', '')}",
                institution_id=None,
                asset_id=None,
                recommended_action="Monitorar e agendar reenvio de consultas pendentes.",
            ))
        elif info["status"] == "DOWN":
            alerts.append(Alert(
                level=RiskLevel.CRITICO,
                category="INFRAESTRUTURA",
                title=f"API fora do ar: {api_name}",
                description=f"{api_name} inacessível. Consultas pendentes bloqueadas.",
                institution_id=None,
                asset_id=None,
                recommended_action="Contatar suporte. Suspender prazo judicial se aplicável.",
            ))
        findings.append(f"API {api_name}: {info['status']} ({info['latency_ms']}ms)")

    for inst_id, info in _MOCK_HEALTH_STATUS["integrators"].items():
        if info["status"] == "OFFLINE":
            alerts.append(Alert(
                level=RiskLevel.CRITICO,
                category="INTEGRADOR_OFFLINE",
                title=f"Integrador offline: {inst_id}",
                description=(
                    f"Integrador SISBAJUD de {inst_id} offline desde {info['last_seen']}. "
                    "Impossível confirmar resposta ou não resposta."
                ),
                institution_id=inst_id,
                asset_id=None,
                recommended_action=(
                    "Verificar se não resposta configura código 98. "
                    "Notificar juízo e solicitar bloqueio alternativo via BACEN."
                ),
            ))
        findings.append(f"Integrador {inst_id}: {info['status']} (último contato: {info['last_seen']})")

    return alerts, findings


def _check_pl_divergences() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []
    threshold_critical = RISK_THRESHOLDS["drain_ratio_critical"] * 100
    threshold_high = RISK_THRESHOLDS["drain_ratio_high"] * 100

    for div in _MOCK_PL_DIVERGENCES:
        variance = div["variance_pct"]
        inst_id = div["institution_id"]
        asset_id = div["asset_id"]
        flag = div["flag"]

        if variance >= threshold_critical:
            level = RiskLevel.CRITICO
            action = (
                "Petição imediata de fraude à execução (CPC 792). "
                "Solicitar extratos completos. Rastrear destino dos valores."
            )
        elif variance >= threshold_high:
            level = RiskLevel.ALTO
            action = "Solicitar perícia contábil. Cruzar com dados IRPF e CVM."
        else:
            level = RiskLevel.MEDIO
            action = "Monitorar evolução. Incluir na análise de consistência."

        alerts.append(Alert(
            level=level,
            category="DIVERGENCIA_PL",
            title=f"Divergência de PL: {asset_id} ({variance:.1f}%)",
            description=(
                f"Variação de {variance:.1f}% detectada em {asset_id} ({inst_id}). "
                f"Flag: {flag}."
            ),
            institution_id=inst_id,
            asset_id=asset_id,
            recommended_action=action,
        ))
        findings.append(
            f"{asset_id} ({inst_id}): variação de PL {variance:.1f}% — {flag}"
        )

    return alerts, findings


def run() -> ModuleResult:
    api_alerts, api_findings = _check_api_health()
    pl_alerts, pl_findings = _check_pl_divergences()

    all_alerts = api_alerts + pl_alerts
    all_findings = api_findings + pl_findings

    critical_assets = {
        "FRAM XIV FIP": 3_877_255.47,
        "LIG Itaú": 1_250_000.00,
        "CDB BTG": 650_758.60,
    }
    all_findings.append(
        "Ativos marcados como risco crítico: "
        + ", ".join(f"{k} (R$ {v:,.2f})" for k, v in critical_assets.items())
    )

    return ModuleResult(
        module_name="SYSTEM_HEALTH_CHECK",
        status="CRITICO" if any(a.level == RiskLevel.CRITICO for a in all_alerts) else "DEGRADADO",
        alerts=all_alerts,
        findings=all_findings,
        metrics={
            "apis_checked": len(_MOCK_HEALTH_STATUS["apis"]),
            "integrators_checked": len(_MOCK_HEALTH_STATUS["integrators"]),
            "pl_divergences_detected": len(_MOCK_PL_DIVERGENCES),
            "critical_alerts": sum(1 for a in all_alerts if a.level == RiskLevel.CRITICO),
            "total_critical_assets_brl": sum(critical_assets.values()),
        },
        timestamp=datetime.now(),
    )
