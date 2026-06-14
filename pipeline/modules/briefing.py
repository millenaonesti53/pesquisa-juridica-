"""
Módulo 1 — BRIEFING
Agrega contexto humano, síntese jurídica e agenda investigativa.
Carrega o Whole Money Trail e atualiza status das instituições.
"""

from datetime import datetime, date
from typing import Optional

from pipeline.config import INSTITUTIONS_DATA, ASSETS_DATA, SISBAJUD_CODES
from pipeline.models import (
    Alert, Asset, AssetStatus, Institution, InstitutionType,
    ModuleResult, RiskLevel, SisbajudResponse,
)


def _build_institutions() -> list[Institution]:
    institutions = []
    for raw in INSTITUTIONS_DATA["institutions"]:
        assets = [
            Asset(
                id=a["id"],
                name=a["name"],
                asset_type=a["type"],
                institution_id=raw["id"],
                value_brl=a.get("pl_reported"),
                verified_value_brl=a.get("pl_verified"),
                status=AssetStatus.BLOQUEIO_PENDENTE,
                flags=a.get("flags", []),
                impenhorability_claim=a.get("impenhorabilidade_alegada", False),
            )
            for a in raw.get("assets", [])
        ]
        institutions.append(Institution(
            id=raw["id"],
            name=raw["name"],
            institution_type=InstitutionType.BANCO if raw["type"] == "banco" else InstitutionType.GESTORA_FIP,
            sisbajud_code=raw["sisbajud_code"],
            status=AssetStatus[raw["status"]] if raw["status"] in AssetStatus.__members__ else AssetStatus.SUSPEITO,
            risk_level=RiskLevel[raw["risk_level"]],
            assets=assets,
            notes=raw.get("notes", ""),
            legal_frameworks=raw.get("legal_framework", []),
        ))
    return institutions


def _build_whole_money_trail() -> list[Asset]:
    trail = []
    for raw in ASSETS_DATA["whole_money_trail"]["assets"]:
        trail.append(Asset(
            id=raw["id"],
            name=raw["description"],
            asset_type=raw.get("id", "desconhecido"),
            institution_id=raw["institution"],
            value_brl=raw.get("value_brl"),
            verified_value_brl=None,
            status=AssetStatus.BLOQUEIO_PENDENTE,
            flags=raw.get("flags", []),
            impenhorability_claim=raw.get("impenhorability_claim", False),
            legal_basis_seizure=raw.get("legal_basis_seizure"),
        ))
    return trail


def _generate_alerts(institutions: list[Institution]) -> list[Alert]:
    alerts = []
    code_descriptions = SISBAJUD_CODES["codes"]
    risk_flags = SISBAJUD_CODES["risk_flags"]

    for inst in institutions:
        code = inst.sisbajud_code
        if inst.is_non_responsive:
            alerts.append(Alert(
                level=RiskLevel.CRITICO,
                category="SISBAJUD_NAO_RESPOSTA",
                title=f"Não resposta: {inst.name}",
                description=(
                    f"{inst.name} não respondeu à ordem SISBAJUD (Código {code}). "
                    f"{risk_flags.get(code, '')} — Possível ocultação patrimonial."
                ),
                institution_id=inst.id,
                asset_id=None,
                recommended_action=(
                    "Notificar juízo sobre não resposta. "
                    "Solicitar imposição de multa diária (art. 77 § 2º CPC). "
                    "Investigar ativos via CVM e IRPF."
                ),
            ))

        if inst.risk_level == RiskLevel.CRITICO:
            for asset in inst.assets:
                if asset.has_suspicious_drain:
                    alerts.append(Alert(
                        level=RiskLevel.CRITICO,
                        category="ESVAZIAMENTO_TATICO",
                        title=f"Esvaziamento tático confirmado: {asset.name}",
                        description=(
                            f"Variação abrupta detectada em {asset.name} ({inst.name}): "
                            f"R$ {asset.value_brl:,.2f} → R$ {asset.verified_value_brl:,.2f}. "
                            f"Redução de {asset.value_delta:,.2f} ({(asset.value_delta/asset.value_brl)*100:.1f}%)."
                        ),
                        institution_id=inst.id,
                        asset_id=asset.id,
                        recommended_action=(
                            "Petição de fraude à execução (CPC 792). "
                            "Solicitar extratos completos desde a citação. "
                            "Rastrear destino dos valores."
                        ),
                    ))

    return alerts


def run(run_date: Optional[date] = None) -> ModuleResult:
    run_date = run_date or date.today()
    institutions = _build_institutions()
    trail = _build_whole_money_trail()
    alerts = _generate_alerts(institutions)

    total_reported = sum(
        a.value_brl or 0
        for inst in institutions
        for a in inst.assets
        if a.value_brl
    )

    non_responsive = [i for i in institutions if i.is_non_responsive]
    critical_insts = [i for i in institutions if i.risk_level == RiskLevel.CRITICO]

    findings = [
        f"Whole Money Trail carregado: {len(trail)} ativos identificados",
        f"Total patrimonial mapeado: R$ {total_reported:,.2f}",
        f"Instituições sem resposta SISBAJUD: {len(non_responsive)} ({', '.join(i.name for i in non_responsive)})",
        f"Instituições em risco crítico: {len(critical_insts)}",
        f"Alertas gerados: {len(alerts)} ({sum(1 for a in alerts if a.level == RiskLevel.CRITICO)} críticos)",
    ]

    return ModuleResult(
        module_name="BRIEFING",
        status="CONCLUIDO_COM_ALERTAS" if alerts else "CONCLUIDO",
        alerts=alerts,
        findings=findings,
        metrics={
            "total_institutions": len(institutions),
            "non_responsive_institutions": len(non_responsive),
            "critical_institutions": len(critical_insts),
            "total_assets": len(trail),
            "total_reported_brl": total_reported,
            "run_date": str(run_date),
        },
        timestamp=datetime.now(),
    )
