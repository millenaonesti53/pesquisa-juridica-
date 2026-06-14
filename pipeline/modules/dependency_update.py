"""
Módulo 3 — DEPENDENCY UPDATE CHECK
Atualiza bases de dados (CVM, IRPF, extratos, FATCA/CRS, FIPs).
Detecta criação retroativa de classes, side-pockets, SPVs novas.
"""

from datetime import datetime, date
from typing import Optional

from pipeline.models import Alert, ModuleResult, RiskLevel


_MOCK_UPDATE_STATUS = {
    "CVM": {
        "last_update": "2026-06-14",
        "records_updated": 847,
        "status": "OK",
    },
    "IRPF_RECEITA": {
        "last_update": "2026-06-13",
        "records_updated": 12,
        "status": "OK",
    },
    "EXTRATOS_BANCARIOS": {
        "last_update": "2026-06-14",
        "records_updated": 234,
        "status": "PARCIAL",
        "missing": ["FRAM", "OSLO"],
    },
    "FATCA_CRS": {
        "last_update": "2026-06-10",
        "records_updated": 3,
        "status": "OK",
    },
    "SISBAJUD_LOGS": {
        "last_update": "2026-06-14",
        "records_updated": 18,
        "status": "OK",
    },
}

_MOCK_STRUCTURAL_CHANGES = [
    {
        "entity": "FRAM XIV FIP",
        "institution_id": "FRAM",
        "change_type": "CRIACAO_CLASSE_RETROATIVA",
        "description": "Classe J criada retroativamente em 2025-11-10, dois meses após início do litígio (2025-09-15)",
        "date_detected": "2026-06-14",
        "date_change": "2025-11-10",
        "date_litigation_start": "2025-09-15",
        "risk": "CRITICO",
        "legal_basis": ["CPC_792", "Lei_9613_98"],
    },
    {
        "entity": "FRAM XIV FIP",
        "institution_id": "FRAM",
        "change_type": "SIDE_POCKET",
        "description": "Side-pocket criado em FRAM XIV FIP após ordem de bloqueio. Segregação de ativos ilíquidos pode configurar fraude.",
        "date_detected": "2026-06-14",
        "date_change": "2026-01-20",
        "risk": "CRITICO",
        "legal_basis": ["CPC_792", "CC_50"],
    },
    {
        "entity": "Bonifácio FIP",
        "institution_id": "BONIFACIO",
        "change_type": "CRIACAO_FIP_POS_LITIGIO",
        "description": "Bonifácio FIP constituído em 2025-10-05, vinte dias após citação (2025-09-15). Aporte inicial de R$ 2.100.000.",
        "date_detected": "2026-06-14",
        "date_change": "2025-10-05",
        "date_litigation_start": "2025-09-15",
        "risk": "CRITICO",
        "legal_basis": ["CPC_792", "art_171_CP", "Lei_9613_98"],
    },
    {
        "entity": "Ajaccio Fundo de Investimento",
        "institution_id": "AJACCIO",
        "change_type": "INCONSISTENCIA_TEMPORAL",
        "description": "Documentação do Ajaccio apresenta data de constituição inconsistente com registros CVM: diferença de 14 meses.",
        "date_detected": "2026-06-14",
        "risk": "ALTO",
        "legal_basis": ["Lei_9613_98"],
    },
]


def _check_data_sources() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for source, info in _MOCK_UPDATE_STATUS.items():
        status = info["status"]
        if status == "PARCIAL":
            missing = info.get("missing", [])
            alerts.append(Alert(
                level=RiskLevel.ALTO,
                category="DADOS_INCOMPLETOS",
                title=f"Atualização parcial: {source}",
                description=(
                    f"Base {source} atualizada parcialmente. "
                    f"Instituições sem dados: {', '.join(missing)}."
                ),
                institution_id=None,
                asset_id=None,
                recommended_action=(
                    f"Forçar reenvio de consulta para: {', '.join(missing)}. "
                    "Considerar ofício ao BACEN para dados complementares."
                ),
            ))
        findings.append(
            f"{source}: {status} — {info['records_updated']} registros (última atualização: {info['last_update']})"
        )

    return alerts, findings


def _check_structural_changes() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for change in _MOCK_STRUCTURAL_CHANGES:
        level = RiskLevel[change["risk"]]
        legal = ", ".join(change["legal_basis"])

        alerts.append(Alert(
            level=level,
            category=f"MUDANCA_ESTRUTURAL_{change['change_type']}",
            title=f"{change['change_type'].replace('_', ' ')}: {change['entity']}",
            description=change["description"],
            institution_id=change["institution_id"],
            asset_id=None,
            recommended_action=(
                f"Enquadramento jurídico: {legal}. "
                "Incluir em relatório de fraude à execução. "
                "Solicitar perícia na documentação do fundo."
            ),
        ))
        findings.append(
            f"[{level.value}] {change['entity']}: {change['change_type']} detectado em {change['date_detected']}"
        )

    return alerts, findings


def run() -> ModuleResult:
    source_alerts, source_findings = _check_data_sources()
    struct_alerts, struct_findings = _check_structural_changes()

    all_alerts = source_alerts + struct_alerts
    all_findings = source_findings + struct_findings

    critical_changes = [c for c in _MOCK_STRUCTURAL_CHANGES if c["risk"] == "CRITICO"]
    all_findings.append(
        f"Mudanças estruturais críticas pós-litígio: {len(critical_changes)} detectadas"
    )

    return ModuleResult(
        module_name="DEPENDENCY_UPDATE_CHECK",
        status="CRITICO" if any(a.level == RiskLevel.CRITICO for a in all_alerts) else "ALERTA",
        alerts=all_alerts,
        findings=all_findings,
        metrics={
            "data_sources_checked": len(_MOCK_UPDATE_STATUS),
            "structural_changes_detected": len(_MOCK_STRUCTURAL_CHANGES),
            "critical_changes": len(critical_changes),
            "total_records_updated": sum(v["records_updated"] for v in _MOCK_UPDATE_STATUS.values()),
        },
        timestamp=datetime.now(),
    )
