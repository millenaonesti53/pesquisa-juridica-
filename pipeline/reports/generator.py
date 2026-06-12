"""
Report Generator — Corporate Cognitive Pipeline.

Produces executive summaries, full text reports, and JSON exports from the
orchestrator output dict. Used by main.py to write reports to disk.

Output formats:
    - Executive summary (brief text, ~1 page)
    - Full report (detailed text, all module findings)
    - JSON export (machine-readable, full data)
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from config.settings import PIPELINE_NAME, PIPELINE_VERSION, REPORT_DATETIME_FORMAT
from pipeline.models import Alert, PipelineReport, RiskLevel, WholeMoneyTrail


def _decimal_serialiser(obj: Any) -> Any:
    """JSON serialiser for Decimal and datetime objects."""
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.strftime(REPORT_DATETIME_FORMAT)
    raise TypeError(f"Object of type {type(obj)} is not JSON serialisable")


class ReportGenerator:
    """Generates human-readable and machine-readable reports from pipeline output.

    Usage::

        gen = ReportGenerator()
        summary = gen.generate_executive_summary(orchestrator_output)
        full = gen.generate_full_report(orchestrator_output)
        gen.export_json(orchestrator_output, "/tmp/report.json")
    """

    SEP_HEAVY = "=" * 72
    SEP_LIGHT = "-" * 72

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def generate_executive_summary(self, orchestrator_output: dict[str, Any]) -> str:
        """Generate a one-page executive summary.

        Args:
            orchestrator_output: Dict returned by
                :meth:`PipelineOrchestrator.run`.

        Returns:
            Formatted text string.
        """
        summary = orchestrator_output.get("summary", {})
        all_alerts: list[Alert] = orchestrator_output.get("all_alerts", [])
        trail: WholeMoneyTrail | None = orchestrator_output.get("trail")
        elapsed = orchestrator_output.get("elapsed_seconds", 0.0)

        now = datetime.utcnow().strftime(REPORT_DATETIME_FORMAT)
        lines: list[str] = []

        lines.append(self.SEP_HEAVY)
        lines.append(f"  {PIPELINE_NAME} v{PIPELINE_VERSION}")
        lines.append(f"  SUMÁRIO EXECUTIVO")
        lines.append(f"  Gerado em: {now} UTC")
        lines.append(f"  Data de Investigação: {summary.get('run_date', 'N/A')}")
        lines.append(self.SEP_HEAVY)
        lines.append("")

        overall = summary.get("overall_status", "unknown").upper()
        lines.append(f"STATUS GERAL DA INVESTIGAÇÃO: {overall}")
        lines.append("")

        lines.append("PATRIMÔNIO INVESTIGADO (BRL):")
        lines.append(
            f"  Total Rastreado:    R$ {Decimal(summary.get('total_tracked_brl', '0')):>18,.2f}"
        )
        lines.append(
            f"  Total Bloqueado:    R$ {Decimal(summary.get('total_blocked_brl', '0')):>18,.2f}"
        )
        lines.append(
            f"  Total Evadido Est.: R$ {Decimal(summary.get('total_evaded_brl', '0')):>18,.2f}"
        )
        lines.append("")

        lines.append("ALERTAS GERADOS:")
        by_level = summary.get("alerts_by_level", {})
        for lvl in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = by_level.get(lvl, 0)
            lines.append(f"  {lvl:<10}: {count:>4}")
        lines.append(f"  {'TOTAL':<10}: {summary.get('total_unique_alerts', 0):>4}")
        lines.append("")

        lines.append("ALERTAS CRÍTICOS:")
        critical_alerts = [a for a in all_alerts if a.level == RiskLevel.CRITICAL]
        if critical_alerts:
            for a in critical_alerts[:5]:
                lines.append(f"  • [{a.category}] {a.description[:90]}...")
            if len(critical_alerts) > 5:
                lines.append(f"  ... e mais {len(critical_alerts) - 5} alertas críticos.")
        else:
            lines.append("  Nenhum alerta crítico.")
        lines.append("")

        lines.append("STATUS POR MÓDULO:")
        for module, status in summary.get("module_statuses", {}).items():
            lines.append(f"  {module:<30} {status.upper()}")
        lines.append("")

        lines.append(f"Tempo de execução do pipeline: {elapsed:.2f}s")
        lines.append(self.SEP_HEAVY)

        return "\n".join(lines)

    def generate_full_report(self, orchestrator_output: dict[str, Any]) -> str:
        """Generate a detailed full text report.

        Args:
            orchestrator_output: Dict returned by
                :meth:`PipelineOrchestrator.run`.

        Returns:
            Formatted text string.
        """
        reports: dict[str, PipelineReport] = orchestrator_output.get("reports", {})
        all_alerts: list[Alert] = orchestrator_output.get("all_alerts", [])
        trail: WholeMoneyTrail | None = orchestrator_output.get("trail")
        summary = orchestrator_output.get("summary", {})
        elapsed = orchestrator_output.get("elapsed_seconds", 0.0)

        now = datetime.utcnow().strftime(REPORT_DATETIME_FORMAT)
        lines: list[str] = []

        lines.append(self.SEP_HEAVY)
        lines.append(f"  {PIPELINE_NAME} v{PIPELINE_VERSION}")
        lines.append(f"  RELATÓRIO COMPLETO DA INVESTIGAÇÃO PATRIMONIAL")
        lines.append(f"  Gerado em: {now} UTC  |  Duração: {elapsed:.2f}s")
        lines.append(self.SEP_HEAVY)
        lines.append("")

        # ── Section 1: Asset inventory ────────────────────────────────────
        lines.append("SEÇÃO 1 — INVENTÁRIO DE ATIVOS RASTREADOS")
        lines.append(self.SEP_LIGHT)
        if trail:
            for asset in trail.assets:
                lines.append(
                    f"  {asset.name:<30} | {asset.institution:<20} | "
                    f"R$ {asset.value_brl:>14,.2f} | {asset.status.value.upper():<14} | "
                    f"SISBAJUD: {asset.sisbajud_code.value if asset.sisbajud_code else 'N/A'} | "
                    f"Risco: {asset.risk_level.name}"
                )
        lines.append("")

        # ── Section 2: Institutions ───────────────────────────────────────
        lines.append("SEÇÃO 2 — INSTITUIÇÕES SOB VIGILÂNCIA")
        lines.append(self.SEP_LIGHT)
        if trail:
            for inst in trail.institutions:
                latest = inst.latest_balance()
                prev = inst.previous_balance()
                lines.append(
                    f"  {inst.name:<25} | Tipo: {inst.type:<15} | "
                    f"SISBAJUD: {inst.sisbajud_code.value if inst.sisbajud_code else 'N/A'} | "
                    f"Risco: {inst.risk_level.name}"
                )
                if latest is not None:
                    lines.append(
                        f"    Saldo atual: R$ {latest:,.2f}"
                        + (f"  (anterior: R$ {prev:,.2f})" if prev else "")
                    )
        lines.append("")

        # ── Section 3: All alerts ─────────────────────────────────────────
        lines.append("SEÇÃO 3 — TODOS OS ALERTAS (ORDENADOS POR CRITICIDADE)")
        lines.append(self.SEP_LIGHT)
        for i, alert in enumerate(all_alerts, 1):
            lines.append(
                f"\n  [{i:>3}] [{alert.level.name}] {alert.category}"
            )
            lines.append(f"        Módulo:      {alert.module}")
            if alert.institution:
                lines.append(f"        Instituição: {alert.institution}")
            if alert.asset:
                lines.append(f"        Ativo:       {alert.asset.name}")
            lines.append(f"        Descrição:   {alert.description}")
            if alert.recommended_action:
                lines.append(f"        Ação:        {alert.recommended_action}")
            if alert.legal_refs:
                lines.append(f"        Base Legal:  {', '.join(alert.legal_refs)}")
        lines.append("")

        # ── Section 4: Module findings ────────────────────────────────────
        lines.append("SEÇÃO 4 — ACHADOS POR MÓDULO")
        lines.append(self.SEP_LIGHT)
        for module_name, report in reports.items():
            lines.append(f"\n  [ {module_name} ] — Status: {report.status.upper()}")
            lines.append(f"  Alertas: {len(report.alerts)}")
            for key, val in report.findings.items():
                if isinstance(val, (str, int, float)):
                    lines.append(f"    {key}: {val}")
                elif isinstance(val, list) and all(isinstance(v, str) for v in val):
                    lines.append(f"    {key}: {', '.join(val)}")
            if report.recommendations:
                lines.append(f"  Recomendações:")
                for rec in report.recommendations:
                    lines.append(f"    • {rec}")
        lines.append("")

        # ── Section 5: CLO report (from PR_REVIEW_DIGEST) ─────────────────
        digest = reports.get("PR_REVIEW_DIGEST")
        if digest:
            clo_report = digest.findings.get("clo_report", "")
            coaf_brief = digest.findings.get("coaf_mpf_brief", "")
            if clo_report:
                lines.append("SEÇÃO 5 — RELATÓRIO CLO")
                lines.append(self.SEP_LIGHT)
                lines.append(clo_report)
                lines.append("")
            if coaf_brief:
                lines.append("SEÇÃO 6 — BRIEF COAF/MPF")
                lines.append(self.SEP_LIGHT)
                lines.append(coaf_brief)
                lines.append("")

        lines.append(self.SEP_HEAVY)
        lines.append("  FIM DO RELATÓRIO")
        lines.append(self.SEP_HEAVY)

        return "\n".join(lines)

    def export_json(self, orchestrator_output: dict[str, Any], path: str) -> None:
        """Save a JSON-serialisable representation of the orchestrator output.

        Args:
            orchestrator_output: Dict returned by
                :meth:`PipelineOrchestrator.run`.
            path: Absolute or relative file path for the JSON file.
        """
        # Build a JSON-safe version (no raw dataclass objects)
        trail: WholeMoneyTrail | None = orchestrator_output.get("trail")
        reports: dict[str, PipelineReport] = orchestrator_output.get("reports", {})
        all_alerts: list[Alert] = orchestrator_output.get("all_alerts", [])
        summary = orchestrator_output.get("summary", {})
        elapsed = orchestrator_output.get("elapsed_seconds", 0.0)

        def serialise_alert(a: Alert) -> dict:
            return {
                "id": a.id,
                "timestamp": a.timestamp.strftime(REPORT_DATETIME_FORMAT),
                "level": a.level.name,
                "category": a.category,
                "description": a.description,
                "institution": a.institution,
                "asset_name": a.asset.name if a.asset else None,
                "legal_refs": a.legal_refs,
                "recommended_action": a.recommended_action,
                "module": a.module,
            }

        def serialise_report(r: PipelineReport) -> dict:
            return {
                "module": r.module,
                "status": r.status,
                "timestamp": r.timestamp.strftime(REPORT_DATETIME_FORMAT),
                "findings": _safe_findings(r.findings),
                "alerts": [serialise_alert(a) for a in r.alerts],
                "recommendations": r.recommendations,
            }

        def _safe_findings(findings: dict) -> dict:
            """Recursively make findings JSON-serialisable."""
            result: dict = {}
            for k, v in findings.items():
                if isinstance(v, Decimal):
                    result[k] = str(v)
                elif isinstance(v, dict):
                    result[k] = _safe_findings(v)
                elif isinstance(v, list):
                    result[k] = [
                        _safe_findings(item) if isinstance(item, dict)
                        else str(item) if isinstance(item, Decimal)
                        else item
                        for item in v
                    ]
                else:
                    result[k] = v
            return result

        payload: dict = {
            "pipeline": {
                "name": PIPELINE_NAME,
                "version": PIPELINE_VERSION,
                "elapsed_seconds": elapsed,
            },
            "summary": summary,
            "assets": [
                {
                    "id": a.id,
                    "name": a.name,
                    "institution": a.institution,
                    "value_brl": str(a.value_brl),
                    "asset_type": a.asset_type,
                    "status": a.status.value,
                    "sisbajud_code": a.sisbajud_code.value if a.sisbajud_code else None,
                    "risk_level": a.risk_level.name,
                    "notes": a.notes,
                    "creation_date": a.creation_date,
                    "is_post_litigation": a.is_post_litigation,
                }
                for a in (trail.assets if trail else [])
            ],
            "institutions": [
                {
                    "name": i.name,
                    "type": i.type,
                    "sisbajud_code": i.sisbajud_code.value if i.sisbajud_code else None,
                    "last_response": i.last_response,
                    "balance_history": [
                        {"date": d, "balance_brl": str(b)}
                        for d, b in i.balance_history
                    ],
                    "risk_level": i.risk_level.name,
                }
                for i in (trail.institutions if trail else [])
            ],
            "reports": {name: serialise_report(r) for name, r in reports.items()},
            "all_alerts": [serialise_alert(a) for a in all_alerts],
        }

        # Ensure output directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, default=_decimal_serialiser)
