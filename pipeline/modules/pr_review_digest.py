"""
Módulo 5 — PR REVIEW DIGEST
Consolida relatórios, pareceres e decisões jurídicas pendentes.
Gera mapa de ativos penhoráveis e minutas para COAF/MPF/CLO.
"""

from datetime import datetime
from typing import Optional

from pipeline.config import LEGAL_FRAMEWORKS, REPORTING_TARGETS, ASSETS_DATA
from pipeline.models import Alert, Asset, ModuleResult, RiskLevel


_PENDING_LEGAL_ACTIONS = [
    {
        "id": "PET_001",
        "type": "PETICAO_FRAUDE_EXECUCAO",
        "title": "Petição de Fraude à Execução — Itaú/BTG",
        "status": "RASCUNHO",
        "priority": "CRITICA",
        "framework": "CPC_792",
        "evidence": [
            "Esvaziamento R$ 463.409 no dia da citação (CC Itaú)",
            "Saldo zero imediato pós-citação (CDB BTG R$ 650.758,60)",
            "Série temporal demonstra padrão coordenado",
        ],
        "target_recipient": "CLO",
        "deadline": "2026-06-17",
    },
    {
        "id": "PET_002",
        "type": "DESCONSIDERACAO_PERSONALIDADE_JURIDICA",
        "title": "Pedido de Desconsideração da Personalidade Jurídica — Bonifácio FIP",
        "status": "EM_ELABORACAO",
        "priority": "CRITICA",
        "framework": "CC_50",
        "evidence": [
            "FIP criado 20 dias após citação",
            "Aporte inicial R$ 2.100.000 de origem não esclarecida",
            "Confusão patrimonial entre executado e FIP",
        ],
        "target_recipient": "IDPJ",
        "deadline": "2026-06-20",
    },
    {
        "id": "REL_001",
        "type": "RELATORIO_COAF",
        "title": "Relatório de Operações Suspeitas — COAF",
        "status": "PENDENTE",
        "priority": "ALTA",
        "framework": "Lei_9613_98",
        "evidence": [
            "Movimentações suspeitas em FRAM XIV FIP",
            "Side-pocket pós-ordem judicial",
            "Classe J criada retroativamente",
            "Criação de FIP (Bonifácio) pós-litígio",
        ],
        "target_recipient": "COAF",
        "deadline": "2026-06-28",
    },
    {
        "id": "PAR_001",
        "type": "PARECER_IMPENHORABILIDADE_LIG",
        "title": "Parecer sobre Penhorabilidade da LIG Itaú (R$ 1.250.000)",
        "status": "EM_REVISAO",
        "priority": "ALTA",
        "framework": "CPC_792",
        "evidence": [
            "Precedente STJ: REsp 1.900.346 — LIG penhorável quando não vinculada a contrato específico",
            "Itaú não apresentou demonstrativo de vínculo contratual",
            "Alegação genérica de impenhorabilidade insuficiente",
        ],
        "target_recipient": "CLO",
        "deadline": "2026-06-18",
    },
    {
        "id": "MAP_001",
        "type": "MAPA_ATIVOS_PENHORAVEIS",
        "title": "Mapa de Ativos Penhoráveis — Atualização",
        "status": "PENDENTE",
        "priority": "ALTA",
        "framework": "CPC_792",
        "evidence": [],
        "target_recipient": "CLO",
        "deadline": "2026-06-15",
    },
]

_SEIZURE_MAP = [
    {
        "asset_id": "FRAM_XIV_FIP",
        "description": "FRAM XIV FIP — Cotas de FIP",
        "value_brl": 3_877_255.47,
        "penhorability": "PENHORAVEL",
        "legal_basis": "art. 831 CPC — penhora de cotas de fundo de investimento",
        "obstacles": ["Ausência de resposta SISBAJUD", "Side-pocket alegado"],
        "recommended_action": "Penhora direta via SISBAJUD + ofício à CVM para bloqueio de cotas",
    },
    {
        "asset_id": "LIG_ITAU",
        "description": "LIG Itaú — Letra Imobiliária Garantida",
        "value_brl": 1_250_000.00,
        "penhorability": "CONTESTAVEL",
        "legal_basis": "STJ REsp 1.900.346 — LIG penhorável quando não vinculada",
        "obstacles": ["Alegação de impenhorabilidade pelo Itaú"],
        "recommended_action": "Parecer jurídico + petição contestando impenhorabilidade + penhora cautelar",
    },
    {
        "asset_id": "CDB_BTG",
        "description": "CDB BTG Pactual",
        "value_brl": 650_758.60,
        "penhorability": "PENHORAVEL",
        "legal_basis": "art. 831 CPC — penhora de aplicações financeiras",
        "obstacles": ["Saldo zero suspeito — rastrear destino"],
        "recommended_action": "Fraude à execução (CPC 792) + rastreamento via extrato + bloqueio do destinatário",
    },
    {
        "asset_id": "CC_ITAU_ANTERIOR",
        "description": "Conta Corrente Itaú — recomposição por fraude à execução",
        "value_brl": 469_575.00,
        "penhorability": "PENHORAVEL_VIA_FRAUDE_EXECUCAO",
        "legal_basis": "CPC 792 — ineficácia do ato de esvaziamento",
        "obstacles": ["Necessidade de petição de fraude à execução"],
        "recommended_action": "Petição imediata de fraude à execução + rastreamento DOC/TED 15/09/2025",
    },
]


def _review_pending_actions() -> tuple[list[Alert], list[str]]:
    alerts = []
    findings = []

    for action in _PENDING_LEGAL_ACTIONS:
        priority = action["priority"]
        level = RiskLevel.CRITICO if priority == "CRITICA" else RiskLevel.ALTO

        framework_info = LEGAL_FRAMEWORKS.get(action["framework"], {})
        target = REPORTING_TARGETS.get(action["target_recipient"], action["target_recipient"])

        alerts.append(Alert(
            level=level,
            category=f"ACAO_JURIDICA_{action['type']}",
            title=f"[{action['status']}] {action['title']}",
            description=(
                f"Prazo: {action['deadline']} | Destinatário: {target} | "
                f"Base: {framework_info.get('description', action['framework'])} | "
                f"Evidências: {len(action['evidence'])} documentadas."
            ),
            institution_id=None,
            asset_id=None,
            recommended_action=f"Finalizar e encaminhar para {target} até {action['deadline']}.",
        ))
        findings.append(
            f"[{action['status']}] {action['title']} — prazo: {action['deadline']}"
        )

    return alerts, findings


def _build_seizure_map_summary() -> list[str]:
    findings = []
    total_penhoravel = sum(
        a["value_brl"] for a in _SEIZURE_MAP if a["penhorability"] in ("PENHORAVEL", "PENHORAVEL_VIA_FRAUDE_EXECUCAO")
    )
    total_contestavel = sum(
        a["value_brl"] for a in _SEIZURE_MAP if a["penhorability"] == "CONTESTAVEL"
    )

    findings.append(f"MAPA DE ATIVOS PENHORÁVEIS:")
    for asset in _SEIZURE_MAP:
        findings.append(
            f"  • {asset['description']}: R$ {asset['value_brl']:,.2f} [{asset['penhorability']}]"
        )
    findings.append(f"Total confirmado penhorável: R$ {total_penhoravel:,.2f}")
    findings.append(f"Total contestável/em disputa: R$ {total_contestavel:,.2f}")
    findings.append(f"Total mapeado: R$ {total_penhoravel + total_contestavel:,.2f}")

    return findings


def _build_legal_framework_summary() -> list[str]:
    findings = []
    findings.append("ENQUADRAMENTO JURÍDICO:")
    for key, fw in LEGAL_FRAMEWORKS.items():
        findings.append(f"  • {fw['description']}: APLICÁVEL")
    return findings


def run() -> ModuleResult:
    action_alerts, action_findings = _review_pending_actions()
    seizure_findings = _build_seizure_map_summary()
    legal_findings = _build_legal_framework_summary()

    all_findings = action_findings + seizure_findings + legal_findings

    total_penhoravel = sum(
        a["value_brl"] for a in _SEIZURE_MAP
        if a["penhorability"] in ("PENHORAVEL", "PENHORAVEL_VIA_FRAUDE_EXECUCAO")
    )
    total_contestavel = sum(
        a["value_brl"] for a in _SEIZURE_MAP if a["penhorability"] == "CONTESTAVEL"
    )

    critical_actions = [a for a in _PENDING_LEGAL_ACTIONS if a["priority"] == "CRITICA"]

    return ModuleResult(
        module_name="PR_REVIEW_DIGEST",
        status="CRITICO" if critical_actions else "ALERTA",
        alerts=action_alerts,
        findings=all_findings,
        metrics={
            "pending_legal_actions": len(_PENDING_LEGAL_ACTIONS),
            "critical_actions": len(critical_actions),
            "seizure_map_assets": len(_SEIZURE_MAP),
            "total_penhoravel_brl": total_penhoravel,
            "total_contestavel_brl": total_contestavel,
            "total_mapped_brl": total_penhoravel + total_contestavel,
            "legal_frameworks_applicable": len(LEGAL_FRAMEWORKS),
        },
        timestamp=datetime.now(),
    )
