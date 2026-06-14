"""
Módulo 4 — FLAKY TEST TRACKER
Identifica inconsistências estatísticas: PLs variando sem justificativa,
respostas bancárias incoerentes, padrões de esvaziamento pré-ordem.
"""

from datetime import datetime
from typing import Optional

from pipeline.models import Alert, ModuleResult, RiskLevel


_MOCK_BEHAVIORAL_SERIES = [
    {
        "institution_id": "BTG",
        "asset_id": "CDB_BTG",
        "name": "CDB BTG Pactual",
        "series": [
            {"date": "2025-08-01", "balance": 650_758.60},
            {"date": "2025-08-15", "balance": 648_200.00},
            {"date": "2025-09-01", "balance": 652_100.00},
            {"date": "2025-09-10", "balance": 651_400.00},
            {"date": "2025-09-15", "balance": 0.00, "note": "Data da citação"},
            {"date": "2025-09-20", "balance": 0.00},
            {"date": "2025-10-01", "balance": 0.00},
            {"date": "2026-01-01", "balance": 0.00},
            {"date": "2026-06-14", "balance": 0.00},
        ],
        "pattern": "SALDO_ZERO_IMEDIATO_POS_CITACAO",
        "flags": ["saldo_zero_repetido", "movimentacao_previa_confirmada"],
    },
    {
        "institution_id": "ITAU",
        "asset_id": "CC_ITAU",
        "name": "Conta Corrente Itaú",
        "series": [
            {"date": "2025-08-01", "balance": 470_000.00},
            {"date": "2025-09-01", "balance": 469_575.00},
            {"date": "2025-09-14", "balance": 468_900.00, "note": "Véspera da citação"},
            {"date": "2025-09-15", "balance": 5_491.00, "note": "Dia da citação – esvaziamento de R$ 463.409"},
            {"date": "2025-09-20", "balance": 5_200.00},
            {"date": "2026-06-14", "balance": 5_491.00},
        ],
        "pattern": "ESVAZIAMENTO_DIA_CITACAO",
        "flags": ["variacao_abrupta", "esvaziamento_tatico_confirmado"],
    },
    {
        "institution_id": "FRAM",
        "asset_id": "FRAM_XIV_FIP",
        "name": "FRAM XIV FIP",
        "series": [
            {"date": "2025-06-01", "balance": 3_900_000.00},
            {"date": "2025-07-01", "balance": 3_877_255.47},
            {"date": "2025-09-15", "balance": None, "note": "Sem resposta pós-citação"},
            {"date": "2025-12-01", "balance": None},
            {"date": "2026-06-14", "balance": None},
        ],
        "pattern": "AUSENCIA_RESPOSTA_SISTEMATICA",
        "flags": ["ausencia_resposta", "side_pocket", "classe_retroativa"],
    },
    {
        "institution_id": "OSLO",
        "asset_id": None,
        "name": "OSLO Capital",
        "series": [
            {"date": "2025-09-15", "balance": None, "note": "Sem resposta desde a citação"},
            {"date": "2026-06-14", "balance": None},
        ],
        "pattern": "AUSENCIA_RESPOSTA_SISTEMATICA",
        "flags": ["ausencia_resposta"],
    },
]

_ILIQUIDITY_CLAIMS = [
    {
        "institution_id": "FRAM",
        "asset_id": "FRAM_XIV_FIP",
        "claim": "Ativos ilíquidos — FIP com prazo de desinvestimento de 7 anos",
        "consistency_check": {
            "pl_3_months_before": 3_900_000.00,
            "redemptions_detected": False,
            "side_pocket_created": True,
            "class_created_post_litigation": True,
        },
        "verdict": "INCONSISTENTE",
        "analysis": (
            "Alegação de iliquidez inconsistente com PL estável R$ 3.877.255 nos 3 meses anteriores. "
            "Criação de side-pocket e Classe J após litígio sugere reconfiguração tática para alegar iliquidez."
        ),
    },
    {
        "institution_id": "ITAU",
        "asset_id": "LIG_ITAU",
        "claim": "LIG é impenhorável por ser garantia real vinculada",
        "consistency_check": {
            "specific_contract_found": False,
            "stj_precedent": "REsp 1.900.346 — LIG penhorável quando não vinculada a contrato específico",
        },
        "verdict": "CONTESTAVEL",
        "analysis": (
            "Impenhorabilidade da LIG é contestável. STJ admite penhora quando não há vínculo "
            "com contrato de financiamento específico. Solicitar demonstrativo de vínculo."
        ),
    },
]


def _analyze_behavioral_series() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for series_data in _MOCK_BEHAVIORAL_SERIES:
        pattern = series_data["pattern"]
        name = series_data["name"]
        inst_id = series_data["institution_id"]
        asset_id = series_data.get("asset_id")

        if pattern == "ESVAZIAMENTO_DIA_CITACAO":
            pre = next((s["balance"] for s in series_data["series"] if "Véspera" in s.get("note", "")), None)
            post = next((s["balance"] for s in series_data["series"] if "Dia da citação" in s.get("note", "") and s["balance"] is not None), None)

            if pre and post is not None:
                drained = pre - post
                alerts.append(Alert(
                    level=RiskLevel.CRITICO,
                    category="FLAKY_ESVAZIAMENTO_TATICO",
                    title=f"Esvaziamento no dia da citação: {name}",
                    description=(
                        f"Padrão FLAKY confirmado em {name}: R$ {pre:,.2f} → R$ {post:,.2f} "
                        f"no dia da citação (15/09/2025). "
                        f"R$ {drained:,.2f} retirados em menos de 24h."
                    ),
                    institution_id=inst_id,
                    asset_id=asset_id,
                    recommended_action=(
                        "Petição de fraude à execução (CPC 792) com evidência estatística. "
                        "Solicitar DOC/TED do dia 15/09/2025. "
                        "Rastrear beneficiário da transferência."
                    ),
                ))
                findings.append(f"[CRÍTICO] {name}: esvaziamento de R$ {drained:,.2f} no dia da citação")

        elif pattern == "SALDO_ZERO_IMEDIATO_POS_CITACAO":
            alerts.append(Alert(
                level=RiskLevel.CRITICO,
                category="FLAKY_SALDO_ZERO",
                title=f"Saldo zero imediato pós-citação: {name}",
                description=(
                    f"Padrão FLAKY: {name} apresentou saldo zero imediatamente após citação "
                    f"(15/09/2025), com saldo estável de ~R$ 651.000 nos meses anteriores. "
                    "Esvaziamento tático confirmado por série temporal."
                ),
                institution_id=inst_id,
                asset_id=asset_id,
                recommended_action=(
                    "Solicitar extrato completo desde jan/2025. "
                    "Rastrear destino dos R$ 650.758,60. "
                    "Incluir na petição de fraude à execução."
                ),
            ))
            findings.append(f"[CRÍTICO] {name}: saldo zero pós-citação — esvaziamento tático por série temporal")

        elif pattern == "AUSENCIA_RESPOSTA_SISTEMATICA":
            alerts.append(Alert(
                level=RiskLevel.CRITICO,
                category="FLAKY_AUSENCIA_RESPOSTA",
                title=f"Ausência sistemática de resposta: {name}",
                description=(
                    f"Padrão FLAKY: {name} não responde ao SISBAJUD desde a citação. "
                    "Silêncio sistemático pode configurar desobediência (art. 77 CPC) "
                    "e ocultação patrimonial (Lei 9.613/98)."
                ),
                institution_id=inst_id,
                asset_id=asset_id,
                recommended_action=(
                    "Notificar juízo sobre desobediência. "
                    "Solicitar multa diária (art. 77 § 2º CPC). "
                    "Ofício ao BACEN para dados alternativos."
                ),
            ))
            findings.append(f"[CRÍTICO] {name}: ausência sistemática de resposta desde 15/09/2025")

    return alerts, findings


def _analyze_iliquidity_claims() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for claim in _ILIQUIDITY_CLAIMS:
        verdict = claim["verdict"]
        level = RiskLevel.CRITICO if verdict == "INCONSISTENTE" else RiskLevel.ALTO

        alerts.append(Alert(
            level=level,
            category="FLAKY_ALEGACAO_ILIQUIDEZ",
            title=f"Alegação de iliquidez {verdict}: {claim['asset_id']}",
            description=claim["analysis"],
            institution_id=claim["institution_id"],
            asset_id=claim["asset_id"],
            recommended_action=(
                "Contestar alegação de iliquidez/impenhorabilidade em petição. "
                "Incluir análise estatística como prova. "
                "Solicitar perícia contábil independente."
            ),
        ))
        findings.append(
            f"[{level.value}] Alegação de {claim['institution_id']}: {verdict} — {claim['claim'][:60]}..."
        )

    return alerts, findings


def run() -> ModuleResult:
    series_alerts, series_findings = _analyze_behavioral_series()
    claim_alerts, claim_findings = _analyze_iliquidity_claims()

    all_alerts = series_alerts + claim_alerts
    all_findings = series_findings + claim_findings

    patterns_detected = list({s["pattern"] for s in _MOCK_BEHAVIORAL_SERIES})
    all_findings.append(f"Padrões flaky detectados: {', '.join(patterns_detected)}")

    return ModuleResult(
        module_name="FLAKY_TEST_TRACKER",
        status="CRITICO" if any(a.level == RiskLevel.CRITICO for a in all_alerts) else "ALERTA",
        alerts=all_alerts,
        findings=all_findings,
        metrics={
            "series_analyzed": len(_MOCK_BEHAVIORAL_SERIES),
            "iliquidity_claims_checked": len(_ILIQUIDITY_CLAIMS),
            "critical_patterns": sum(1 for a in all_alerts if a.level == RiskLevel.CRITICO),
            "patterns_detected": patterns_detected,
        },
        timestamp=datetime.now(),
    )
