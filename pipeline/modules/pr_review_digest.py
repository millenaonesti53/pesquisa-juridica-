"""
PR Review Digest Module — Corporate Cognitive Pipeline.

Consolidates findings from all prior pipeline modules into:
    1. A structured criminal-exposure assessment mapped to applicable laws.
    2. A CLO (Chief Legal Officer) executive brief.
    3. A COAF / Federal Prosecutors (MPF) action brief.
    4. A list of immediately attachable assets.

Legal framework implemented:
    - Art. 171 CP   — Estelionato (criminal fraud)
    - Art. 792 CPC  — Fraude à Execução (fraud against execution)
    - Art. 50 CC    — Desconsideração da Personalidade Jurídica
    - Lei 9.613/98  — Lavagem de Dinheiro (money laundering)
    - FATCA/CRS     — Reporte Internacional de Ativos no Exterior
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from config.settings import LEGAL_REFS, PIPELINE_NAME, PIPELINE_VERSION
from pipeline.models import (
    Alert,
    Asset,
    AssetStatus,
    PipelineReport,
    RiskLevel,
    SisbajudCode,
    WholeMoneyTrail,
)

MODULE_NAME = "PR_REVIEW_DIGEST"


# ---------------------------------------------------------------------------
# Legal framework enumeration
# ---------------------------------------------------------------------------


class LegalFramework(Enum):
    """All applicable legal frameworks for this investigation."""

    ART_171_CP = "Art. 171 CP — Estelionato / Fraude"
    ART_792_CPC = "Art. 792 CPC — Fraude à Execução"
    ART_50_CC = "Art. 50 CC — Desconsideração da Personalidade Jurídica"
    LAW_9613_98 = "Lei 9.613/98 — Lavagem de Dinheiro"
    FATCA_CRS = "FATCA/CRS — Reporte Internacional de Ativos"

    @classmethod
    def from_ref_key(cls, key: str) -> "LegalFramework | None":
        mapping = {
            "art_171_cp": cls.ART_171_CP,
            "art_792_cpc": cls.ART_792_CPC,
            "art_50_cc": cls.ART_50_CC,
            "law_9613_98": cls.LAW_9613_98,
            "fatca_crs": cls.FATCA_CRS,
        }
        return mapping.get(key)


# ---------------------------------------------------------------------------
# Category → legal framework mapping
# ---------------------------------------------------------------------------

_CATEGORY_TO_LAWS: dict[str, list[LegalFramework]] = {
    "non_response": [LegalFramework.ART_792_CPC, LegalFramework.ART_171_CP],
    "sisbajud_non_response": [LegalFramework.ART_792_CPC, LegalFramework.ART_171_CP],
    "tactical_emptying": [LegalFramework.ART_792_CPC, LegalFramework.LAW_9613_98, LegalFramework.ART_171_CP],
    "zero_balance_after_movement": [LegalFramework.ART_171_CP, LegalFramework.LAW_9613_98],
    "post_litigation_creation": [LegalFramework.ART_792_CPC, LegalFramework.ART_50_CC],
    "post_litigation_fip_creation": [LegalFramework.ART_792_CPC, LegalFramework.ART_50_CC, LegalFramework.ART_171_CP],
    "side_pocket_suspected": [LegalFramework.ART_171_CP, LegalFramework.ART_792_CPC, LegalFramework.LAW_9613_98],
    "regulatory_change_classe_j_creation": [LegalFramework.ART_792_CPC, LegalFramework.ART_171_CP],
    "regulatory_change_statute_amendment": [LegalFramework.ART_792_CPC],
    "regulatory_change_fund_creation": [LegalFramework.ART_792_CPC, LegalFramework.ART_50_CC],
    "temporal_inconsistency": [LegalFramework.ART_171_CP, LegalFramework.ART_792_CPC],
    "pl_inconsistency": [LegalFramework.ART_171_CP, LegalFramework.FATCA_CRS],
    "balance_anomaly": [LegalFramework.ART_792_CPC, LegalFramework.LAW_9613_98],
    "illiquidity_claim_inconsistent": [LegalFramework.ART_171_CP, LegalFramework.ART_792_CPC],
    "pre_order_emptying": [LegalFramework.ART_792_CPC, LegalFramework.LAW_9613_98, LegalFramework.ART_171_CP],
}


class PRReviewDigest:
    """Consolidates all pipeline module findings into legal action documents.

    This is the final module in the pipeline. It synthesises all prior
    reports into actionable documents for the CLO and public prosecutors.
    """

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def consolidate_findings(self, reports: list[PipelineReport]) -> dict[str, Any]:
        """Merge findings from all pipeline module reports.

        Args:
            reports: List of :class:`PipelineReport` from all modules.

        Returns:
            Consolidated findings dict with aggregated alert counts,
            per-module status, and combined recommendations.
        """
        all_alerts: list[Alert] = []
        all_recommendations: list[str] = []
        module_statuses: dict[str, str] = {}

        for report in reports:
            all_alerts.extend(report.alerts)
            all_recommendations.extend(report.recommendations)
            module_statuses[report.module] = report.status

        # Deduplicate recommendations preserving order
        seen: set[str] = set()
        unique_recs: list[str] = []
        for rec in all_recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)

        # Aggregate alert counts
        by_level: dict[str, int] = {lvl.name: 0 for lvl in RiskLevel}
        by_category: dict[str, int] = {}
        for alert in all_alerts:
            by_level[alert.level.name] += 1
            by_category[alert.category] = by_category.get(alert.category, 0) + 1

        return {
            "total_alerts": len(all_alerts),
            "alerts_by_level": by_level,
            "alerts_by_category": by_category,
            "module_statuses": module_statuses,
            "unique_recommendations": unique_recs,
            "overall_status": (
                "critical" if by_level["CRITICAL"] > 0
                else "warning" if by_level["HIGH"] > 0
                else "ok"
            ),
        }

    def assess_criminal_exposure(self, alerts: list[Alert]) -> dict[str, Any]:
        """Map each alert category to applicable criminal/civil statutes.

        Args:
            alerts: All alerts from all pipeline modules.

        Returns:
            Dict mapping each :class:`LegalFramework` to a list of supporting
            alerts and an exposure summary.
        """
        exposure: dict[str, dict[str, Any]] = {
            fw.value: {"alerts": [], "count": 0, "max_risk": "LOW"}
            for fw in LegalFramework
        }

        for alert in alerts:
            applicable = _CATEGORY_TO_LAWS.get(alert.category, [])
            if not applicable:
                # Fall back to parsing legal_refs
                for ref in alert.legal_refs:
                    fw = LegalFramework.from_ref_key(ref)
                    if fw:
                        applicable.append(fw)

            for fw in applicable:
                entry = exposure[fw.value]
                entry["alerts"].append(
                    {
                        "id": alert.id,
                        "category": alert.category,
                        "level": alert.level.name,
                        "institution": alert.institution,
                        "description_excerpt": alert.description[:120],
                    }
                )
                entry["count"] += 1
                # Track max risk level seen for this law
                current_max = RiskLevel[entry["max_risk"]]
                if alert.level > current_max:
                    entry["max_risk"] = alert.level.name

        # Add summary verdict for each framework
        for fw_label, data in exposure.items():
            if data["count"] == 0:
                data["verdict"] = "SEM EVIDÊNCIAS"
            elif data["max_risk"] == "CRITICAL":
                data["verdict"] = "EXPOSIÇÃO CRÍTICA — REPRESENTAÇÃO IMEDIATA RECOMENDADA"
            elif data["max_risk"] == "HIGH":
                data["verdict"] = "EXPOSIÇÃO ALTA — MONITORAMENTO INTENSIVO"
            else:
                data["verdict"] = "EXPOSIÇÃO MODERADA — DOCUMENTAR E ACOMPANHAR"

        return exposure

    def generate_clo_report(self, findings: dict[str, Any]) -> str:
        """Generate a formatted executive report for the Chief Legal Officer.

        Args:
            findings: Consolidated findings dict from :meth:`consolidate_findings`.

        Returns:
            Formatted text report string.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        lines: list[str] = []
        sep = "=" * 72

        lines.append(sep)
        lines.append(f"  {PIPELINE_NAME} v{PIPELINE_VERSION}")
        lines.append(f"  RELATÓRIO EXECUTIVO — DESTINATÁRIO: CLO (Chief Legal Officer)")
        lines.append(f"  Gerado em: {now}")
        lines.append(sep)
        lines.append("")
        lines.append("1. RESUMO EXECUTIVO")
        lines.append("-" * 40)
        lines.append(
            f"   Status geral da investigação: {findings['overall_status'].upper()}"
        )
        lines.append(f"   Total de alertas gerados: {findings['total_alerts']}")

        by_level = findings.get("alerts_by_level", {})
        lines.append(
            f"   - Críticos:  {by_level.get('CRITICAL', 0)}"
        )
        lines.append(
            f"   - Altos:     {by_level.get('HIGH', 0)}"
        )
        lines.append(
            f"   - Médios:    {by_level.get('MEDIUM', 0)}"
        )
        lines.append(
            f"   - Baixos:    {by_level.get('LOW', 0)}"
        )
        lines.append("")

        lines.append("2. STATUS POR MÓDULO")
        lines.append("-" * 40)
        for module, status in findings.get("module_statuses", {}).items():
            status_icon = "🔴" if status == "critical" else "🟡" if status == "warning" else "🟢"
            lines.append(f"   {module:<30} {status.upper()}")
        lines.append("")

        lines.append("3. CATEGORIAS DE ALERTA IDENTIFICADAS")
        lines.append("-" * 40)
        for cat, count in sorted(
            findings.get("alerts_by_category", {}).items(),
            key=lambda x: -x[1],
        ):
            lines.append(f"   {cat:<45} {count:>3} ocorrência(s)")
        lines.append("")

        lines.append("4. RECOMENDAÇÕES PRIORITÁRIAS")
        lines.append("-" * 40)
        for i, rec in enumerate(findings.get("unique_recommendations", []), 1):
            lines.append(f"   {i:>2}. {rec}")
        lines.append("")

        lines.append("5. ATIVOS RASTREADOS (SUMÁRIO PATRIMONIAL)")
        lines.append("-" * 40)
        lines.append("   (Ver relatório completo para valores individuais)")
        lines.append("")

        lines.append("6. PRÓXIMAS AÇÕES LEGAIS RECOMENDADAS")
        lines.append("-" * 40)
        lines.append("   a) Peticionar tutela de urgência para bloqueio imediato dos ativos FRAM XIV FIP e LIG Itaú.")
        lines.append("   b) Representar ao COAF sobre esvaziamento tático da conta Itaú (R$ 469.575 → R$ 5.491).")
        lines.append("   c) Requerer ao MPF abertura de inquérito por lavagem de dinheiro (Lei 9.613/98).")
        lines.append("   d) Solicitar ao BACEN JUD rastreamento de todas as saídas do BTG Pactual e Itaú.")
        lines.append("   e) Peticionar desconsideração da personalidade jurídica das gestoras não responsivas.")
        lines.append("")
        lines.append(sep)
        lines.append("  DOCUMENTO CONFIDENCIAL — USO RESTRITO À EQUIPE JURÍDICA")
        lines.append(sep)

        return "\n".join(lines)

    def generate_coaf_mpf_brief(self, findings: dict[str, Any]) -> str:
        """Generate a concise brief for COAF and Federal Prosecutors (MPF).

        Args:
            findings: Consolidated findings dict from :meth:`consolidate_findings`.

        Returns:
            Formatted text brief string.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        lines: list[str] = []
        sep = "=" * 72

        lines.append(sep)
        lines.append("  COMUNICAÇÃO DE OPERAÇÃO SUSPEITA")
        lines.append("  Destinatários: COAF / MPF — Força-Tarefa de Lavagem de Dinheiro")
        lines.append(f"  Data: {now}")
        lines.append(sep)
        lines.append("")
        lines.append("IDENTIFICAÇÃO DAS OPERAÇÕES SUSPEITAS:")
        lines.append("")
        lines.append("1. ESVAZIAMENTO TÁTICO PRÉ-JUDICIAL — ITAÚ UNIBANCO")
        lines.append("   Conta corrente com saldo de R$ 469.575,00 foi zerada")
        lines.append("   (R$ 5.491,00 residual) em operação de TED/DOC realizada")
        lines.append("   2 dias antes da ordem judicial de bloqueio SISBAJUD.")
        lines.append("   Tipificação: Art. 792 CPC + Art. 1º da Lei 9.613/98.")
        lines.append("")
        lines.append("2. OCULTAÇÃO DE ATIVO — BTG PACTUAL")
        lines.append("   CDB de R$ 650.758,60 reportado como saldo zero (Código 13)")
        lines.append("   após confirmação de movimentação prévia. Saídas de R$ 650.758,60")
        lines.append("   detectadas 2 dias antes da ordem judicial.")
        lines.append("   Tipificação: Art. 171 CP + Art. 1º, §1º da Lei 9.613/98.")
        lines.append("")
        lines.append("3. CRIAÇÃO DE VEÍCULO PÓS-LITÍGIO — BONIFÁCIO FIP")
        lines.append("   Fundo criado 179 dias após início do litígio (2022-09-10),")
        lines.append("   replicando estrutura societária do OSLO FIP. Indica")
        lines.append("   perpetuação de blindagem patrimonial por veículo diverso.")
        lines.append("   Tipificação: Art. 792 CPC + Art. 50 CC.")
        lines.append("")
        lines.append("4. OMISSÃO SISTEMÁTICA — FRAM CAPITAL E OSLO GESTORA")
        lines.append("   Ambas as gestoras retornaram Código 98 (não resposta)")
        lines.append("   em múltiplas consultas SISBAJUD. Valor em risco:")
        lines.append("   FRAM XIV FIP: R$ 3.877.255,47 (side-pocket suspeito).")
        lines.append("   Tipificação: Art. 171 CP + Art. 792 CPC.")
        lines.append("")
        lines.append("PEDIDOS AO COAF:")
        lines.append("   - Abertura de ROS (Relatório de Operação Suspeita)")
        lines.append("   - Rastreamento de TED/DOC via SITRAF/STR")
        lines.append("   - Verificação de beneficiários finais dos FIPs")
        lines.append("   - Verificação de ativos no exterior via FATCA/CRS")
        lines.append("")
        lines.append("PEDIDOS AO MPF:")
        lines.append("   - Instauração de inquérito por lavagem de dinheiro")
        lines.append("   - Representação por estelionato processual (Art. 171 CP)")
        lines.append("   - Cooperação internacional para localização de ativos offshore")
        lines.append("")
        lines.append(sep)

        return "\n".join(lines)

    def map_attachable_assets(self, trail: WholeMoneyTrail) -> list[Asset]:
        """Identify assets that are candidates for immediate judicial attachment.

        An asset is considered attachable if:
            - It has a known positive BRL value, AND
            - It is not already blocked (Code 00), AND
            - It is not in EMPTIED status

        Args:
            trail: The current :class:`WholeMoneyTrail`.

        Returns:
            List of :class:`Asset` objects that can be seized, sorted by value
            descending.
        """
        attachable = [
            a for a in trail.assets
            if a.value_brl > Decimal("0")
            and a.status != AssetStatus.BLOCKED
            and a.status != AssetStatus.EMPTIED
            and a.sisbajud_code != SisbajudCode.CODE_00
        ]
        return sorted(attachable, key=lambda a: a.value_brl, reverse=True)

    def run(
        self,
        trail: WholeMoneyTrail,
        all_reports: list[PipelineReport],
    ) -> PipelineReport:
        """Execute the PR Review Digest and return a final summary report.

        Args:
            trail: The current :class:`WholeMoneyTrail`.
            all_reports: All :class:`PipelineReport` objects from prior modules.

        Returns:
            A :class:`PipelineReport` with full consolidated findings.
        """
        findings = self.consolidate_findings(all_reports)

        # Collect all alerts from all reports
        all_alerts: list[Alert] = []
        for r in all_reports:
            all_alerts.extend(r.alerts)

        exposure = self.assess_criminal_exposure(all_alerts)
        clo_report = self.generate_clo_report(findings)
        coaf_brief = self.generate_coaf_mpf_brief(findings)
        attachable = self.map_attachable_assets(trail)

        total_attachable_value = sum(
            (a.value_brl for a in attachable), Decimal("0.00")
        )

        # Build digest-specific alerts (one per critical exposure)
        digest_alerts: list[Alert] = []
        for fw_label, data in exposure.items():
            if data["count"] > 0 and data["max_risk"] in ("CRITICAL", "HIGH"):
                digest_alerts.append(
                    Alert(
                        level=RiskLevel[data["max_risk"]],
                        category="criminal_exposure",
                        description=(
                            f"Exposição legal identificada — {fw_label}: "
                            f"{data['count']} alerta(s) de suporte. "
                            f"Veredicto: {data['verdict']}."
                        ),
                        legal_refs=list(LEGAL_REFS.keys()),
                        recommended_action=data["verdict"],
                        module=MODULE_NAME,
                    )
                )

        critical_count = sum(1 for a in digest_alerts if a.level == RiskLevel.CRITICAL)
        status = "critical" if critical_count > 0 else "warning"

        return PipelineReport(
            module=MODULE_NAME,
            status=status,
            findings={
                "consolidated_findings": findings,
                "criminal_exposure_summary": {
                    fw: {"count": v["count"], "max_risk": v["max_risk"], "verdict": v["verdict"]}
                    for fw, v in exposure.items()
                },
                "attachable_assets": [
                    {
                        "name": a.name,
                        "institution": a.institution,
                        "value_brl": str(a.value_brl),
                        "asset_type": a.asset_type,
                        "risk_level": a.risk_level.name,
                    }
                    for a in attachable
                ],
                "total_attachable_value_brl": str(total_attachable_value),
                "clo_report": clo_report,
                "coaf_mpf_brief": coaf_brief,
            },
            alerts=digest_alerts,
            recommendations=[
                "Distribuir relatório CLO à equipe jurídica com urgência.",
                "Protocolar comunicação ao COAF imediatamente.",
                "Ajuizar tutela de urgência para bloqueio dos ativos attachable.",
                "Solicitar cooperação internacional via DRCI/MLAT para ativos offshore.",
                "Agendar reunião de estratégia com o MPF em 48 horas.",
            ],
        )


# ---------------------------------------------------------------------------
# Module self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from pipeline.modules.briefing import BriefingModule
    from pipeline.modules.health_check import SystemHealthCheck

    trail, briefing_report = BriefingModule().run()
    hc_report = SystemHealthCheck().run(trail)

    module = PRReviewDigest()
    report = module.run(trail, [briefing_report, hc_report])

    print("=== PR REVIEW DIGEST SELF-TEST ===")
    print(f"Status: {report.status}")
    print(f"Attachable assets: {len(report.findings['attachable_assets'])}")
    for a in report.findings["attachable_assets"]:
        print(f"  {a['name']}: R$ {float(a['value_brl']):,.2f}")
    print(f"\nTotal attachable value: R$ {float(report.findings['total_attachable_value_brl']):,.2f}")
    print("\n--- CLO REPORT EXCERPT ---")
    print(report.findings["clo_report"][:500])
