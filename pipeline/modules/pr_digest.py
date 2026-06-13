"""
Module 5: PR REVIEW DIGEST
Consolidates all reports, legal analyses, and pending decisions.
Generates final outputs: CLO report, IDPJ opinion, COAF/MPF draft,
and map of attachable assets.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
import logging

from config.settings import LEGAL_REFS
from models.alerts import Alert, AlertSeverity
from pipeline.modules.briefing import BriefingReport
from pipeline.modules.health_check import HealthCheckReport
from pipeline.modules.dependency_check import DependencyReport
from pipeline.modules.flaky_tracker import FlakyTrackerReport, FlakyPattern

logger = logging.getLogger(__name__)


@dataclass
class LegalAnalysis:
    framework: str
    article: str
    applicability: str
    evidence_summary: str
    recommended_action: str
    urgency: str  # IMEDIATA / PROXIMA_AUDIENCIA / INSTRUCAO


@dataclass
class PenhorableAsset:
    id: str
    description: str
    institution: str
    estimated_value: Decimal
    legal_basis: str
    contestation_risk: str  # BAIXO / MEDIO / ALTO
    recommended_instrument: str


@dataclass
class PRDigestReport:
    generated_at: datetime
    legal_analyses: list[LegalAnalysis]
    penherable_assets: list[PenhorableAsset]
    total_recoverable: Decimal
    clo_report: str
    idpj_opinion: str
    coaf_mpf_draft: str
    pending_decisions: list[dict] = field(default_factory=list)
    critical_alert_count: int = 0


class PRDigestModule:
    """
    Final governance consolidator.
    Takes outputs from all upstream modules and produces
    actionable legal instruments.
    """

    def run(
        self,
        briefing: BriefingReport,
        health: HealthCheckReport,
        dependencies: DependencyReport,
        flaky: FlakyTrackerReport,
    ) -> PRDigestReport:
        logger.info("[PR DIGEST] Starting governance digest")

        legal_analyses = self._build_legal_analyses(briefing, flaky)
        penherable = self._map_penherable_assets(briefing)
        total_recoverable = sum(a.estimated_value for a in penherable)
        all_alerts = (
            briefing.critical_alerts
            + health.critical_alerts
            + dependencies.alerts
        )
        critical_count = sum(1 for a in all_alerts if a.severity == AlertSeverity.CRITICO)

        clo_report = self._generate_clo_report(briefing, health, dependencies, flaky, penherable)
        idpj_opinion = self._generate_idpj_opinion(legal_analyses)
        coaf_draft = self._generate_coaf_draft(flaky, penherable)
        pending = self._identify_pending_decisions(briefing, health, dependencies)

        report = PRDigestReport(
            generated_at=datetime.now(),
            legal_analyses=legal_analyses,
            penherable_assets=penherable,
            total_recoverable=total_recoverable,
            clo_report=clo_report,
            idpj_opinion=idpj_opinion,
            coaf_mpf_draft=coaf_draft,
            pending_decisions=pending,
            critical_alert_count=critical_count,
        )

        self._log_report(report)
        return report

    def _build_legal_analyses(
        self, briefing: BriefingReport, flaky: FlakyTrackerReport
    ) -> list[LegalAnalysis]:
        analyses = [
            LegalAnalysis(
                framework="Estelionato Processual",
                article=LEGAL_REFS["estelionato"],
                applicability="ALTA",
                evidence_summary=(
                    "Conduta reiterada de esvaziamento patrimonial (BTG, Itaú) "
                    "com criação de estruturas de blindagem (Bonifácio FIP, Classe J). "
                    "Sequência temporal configura dolo específico."
                ),
                recommended_action="Representação criminal ao MPF com evidências de BTG e Itaú",
                urgency="IMEDIATA",
            ),
            LegalAnalysis(
                framework="Fraude à Execução",
                article=LEGAL_REFS["fraude_execucao"],
                applicability="ALTA",
                evidence_summary=(
                    "Transferências patrimoniais após citação válida. "
                    "Bonifácio FIP criado pós-ajuizamento. "
                    "Classe J FRAM XIV: registro retroativo confirmado."
                ),
                recommended_action="Petição de reconhecimento de fraude à execução c/ bloqueio cautelar",
                urgency="IMEDIATA",
            ),
            LegalAnalysis(
                framework="Desconsideração da Personalidade Jurídica",
                article=LEGAL_REFS["desconsideracao_personalidade"],
                applicability="MEDIA",
                evidence_summary=(
                    "SPV Bonifácio Holdings: criada como camada de ocultação. "
                    "Confusão patrimonial entre réu e estrutura FIP."
                ),
                recommended_action="Incidente de desconsideração (CPC 133) para atingir ativos dos FIPs",
                urgency="PROXIMA_AUDIENCIA",
            ),
            LegalAnalysis(
                framework="Lavagem de Dinheiro",
                article=LEGAL_REFS["lavagem_dinheiro"],
                applicability="MEDIA",
                evidence_summary=(
                    "Ocultação de bens de origem lícita mas com finalidade de frustrar "
                    "execução judicial. Uso de FIPs como instrumento de ocultação. "
                    "FATCA/CRS: verificar transferências internacionais."
                ),
                recommended_action="Comunicação ao COAF com mapa de transações suspeitas",
                urgency="INSTRUCAO",
            ),
        ]
        return analyses

    def _map_penherable_assets(self, briefing: BriefingReport) -> list[PenhorableAsset]:
        assets = []
        for asset in briefing.assets:
            if asset.balance > Decimal("1000"):
                contestation = "BAIXO"
                instrument = "Penhora online via SISBAJUD"
                if not asset.is_penherable:
                    contestation = "ALTO"
                    instrument = "Contestar impenhorabilidade + penhora cautelar"
                elif asset.sisbajud_code == 98:
                    contestation = "MEDIO"
                    instrument = "Mandado de busca e apreensão + penhora forçada"

                assets.append(
                    PenhorableAsset(
                        id=asset.id,
                        description=asset.description,
                        institution=asset.institution,
                        estimated_value=asset.balance,
                        legal_basis=f"CPC 835 — {asset.asset_type.value}",
                        contestation_risk=contestation,
                        recommended_instrument=instrument,
                    )
                )
        return assets

    def _generate_clo_report(
        self,
        briefing: BriefingReport,
        health: HealthCheckReport,
        dep: DependencyReport,
        flaky: FlakyTrackerReport,
        penherable: list[PenhorableAsset],
    ) -> str:
        total_ident = briefing.total_identified
        total_penherable = sum(a.estimated_value for a in penherable)
        critical_signals = flaky.critical_signals

        return f"""
╔══════════════════════════════════════════════════════════╗
║          RELATÓRIO CLO — PIPELINE COGNITIVO              ║
║          Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}                ║
╚══════════════════════════════════════════════════════════╝

SITUAÇÃO PATRIMONIAL
  Total identificado:     R${total_ident:>15,.2f}
  Total penhorável:       R${total_penherable:>15,.2f}
  Status geral:           {health.overall_health}

ALERTAS CRÍTICOS
  Instituições s/ resposta: {', '.join(health.non_responsive_institutions)}
  Esvaziamentos táticos:    {len(health.tactical_drains)} detectados
  Sinais críticos (flaky):  {len(critical_signals)} c/ confiança ≥85%
  Ocultação sistemática:    {'SIM ⚠️' if flaky.systematic_concealment_detected else 'NÃO'}

IRREGULARIDADES FIP
  Total:         {len(dep.fip_irregularities)}
  Pós-litígio:   {len(dep.critical_findings)} (CRÍTICO — ação imediata)
  SPVs novas:    {len(dep.new_spvs_detected)}
  Classes retroativas: {len(dep.retroactive_classes)}

RECOMENDAÇÃO IMEDIATA
  1. Petição de fraude à execução (CPC 792) — BTG/Itaú
  2. Incidente de desconsideração — Bonifácio FIP
  3. Representação MPF — estelionato processual
  4. Comunicação COAF — lavagem (Lei 9.613/98)
""".strip()

    def _generate_idpj_opinion(self, analyses: list[LegalAnalysis]) -> str:
        urgent = [a for a in analyses if a.urgency == "IMEDIATA"]
        lines = ["PARECER IDPJ — DESCONSIDERAÇÃO DA PERSONALIDADE JURÍDICA\n"]
        for a in urgent:
            lines.append(f"[{a.framework}] {a.article}")
            lines.append(f"  Aplicabilidade: {a.applicability}")
            lines.append(f"  Evidências: {a.evidence_summary}")
            lines.append(f"  Ação recomendada: {a.recommended_action}\n")
        return "\n".join(lines)

    def _generate_coaf_draft(
        self, flaky: FlakyTrackerReport, penherable: list[PenhorableAsset]
    ) -> str:
        return f"""
MINUTA — COMUNICAÇÃO AO COAF / MPF
Data: {datetime.now().strftime('%d/%m/%Y')}

OBJETO: Comunicação de operações suspeitas de lavagem de ativos
        no contexto de execução judicial frustrada.

FATOS:
  - Esvaziamento tático confirmado: BTG (R$650.758,60) e Itaú (R$464.084,00)
  - Estruturas pós-litígio: Bonifácio FIP + SPV Bonifácio Holdings
  - Não-resposta sistemática: FRAM, OSLO (código SISBAJUD 98)
  - Classe retroativa: FRAM XIV FIP — Classe J

ENQUADRAMENTO LEGAL:
  - Lei 9.613/98, Art. 1° (ocultação de bens)
  - CPC 792 (fraude à execução)
  - CP 171 (estelionato processual)

ATIVOS SUSPEITOS:
  {chr(10).join(f'  - {a.description}: R${a.estimated_value:,.2f}' for a in penherable)}

TOTAL SOB SUSPEITA: R${sum(a.estimated_value for a in penherable):,.2f}

[Aguarda assinatura do CLO e anexação de evidências documentais]
""".strip()

    def _identify_pending_decisions(
        self,
        briefing: BriefingReport,
        health: HealthCheckReport,
        dep: DependencyReport,
    ) -> list[dict]:
        return [
            {
                "decision": "Contestar impenhorabilidade LIG Itaú",
                "deadline": "URGENTE",
                "responsible": "CLO + Advogado processualista",
                "legal_basis": "CPC 835 § único",
            },
            {
                "decision": "Protocolar petição de fraude à execução",
                "deadline": "PRÓXIMA AUDIÊNCIA",
                "responsible": "CLO",
                "legal_basis": "CPC 792",
            },
            {
                "decision": "Requerer mandado de busca e apreensão — FRAM/OSLO",
                "deadline": "URGENTE",
                "responsible": "Advogado + Juízo",
                "legal_basis": "CPC 536 + SISBAJUD",
            },
            {
                "decision": "Incidente de desconsideração — Bonifácio FIP",
                "deadline": "INSTRUÇÃO",
                "responsible": "CLO + IDPJ",
                "legal_basis": "CPC 133 + CC 50",
            },
        ]

    def _log_report(self, report: PRDigestReport) -> None:
        logger.info(
            f"[PR DIGEST] Complete — "
            f"Alertas críticos: {report.critical_alert_count} | "
            f"Total recuperável: R${report.total_recoverable:,.2f} | "
            f"Decisões pendentes: {len(report.pending_decisions)}"
        )
