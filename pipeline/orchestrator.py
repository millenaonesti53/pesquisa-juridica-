"""
Pipeline Orchestrator — Corporate Cognitive Pipeline.

Runs all five pipeline modules in sequence, collecting, deduplicating, and
prioritising alerts. Provides formatted ASCII/rich terminal output showing
pipeline status as it executes.

Pipeline execution order:
    1. BRIEFING          — Load money trail + generate initial alerts
    2. SYSTEM_HEALTH     — API health + data anomaly detection
    3. DEPENDENCY_CHECK  — FIP creation dates, side-pockets, temporal checks
    4. FLAKY_TRACKER     — Statistical flakiness + pre-order emptying
    5. PR_REVIEW_DIGEST  — Consolidation + CLO/COAF reports + exposure map

Usage::

    from pipeline.orchestrator import PipelineOrchestrator
    orch = PipelineOrchestrator()
    result = orch.run("2024-01-15")
"""

from __future__ import annotations

import time
from datetime import datetime
from decimal import Decimal
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from config.settings import PIPELINE_NAME, PIPELINE_VERSION
from pipeline.models import Alert, PipelineReport, RiskLevel, WholeMoneyTrail
from pipeline.modules.briefing import BriefingModule
from pipeline.modules.dependency_check import DependencyCheckModule
from pipeline.modules.flaky_tracker import FlakyTestTracker
from pipeline.modules.health_check import SystemHealthCheck
from pipeline.modules.pr_review_digest import PRReviewDigest

console = Console()

# ANSI-safe status colours for rich
_STATUS_STYLE: dict[str, str] = {
    "ok": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "critical": "bold red",
}

_RISK_STYLE: dict[str, str] = {
    "LOW": "dim white",
    "MEDIUM": "yellow",
    "HIGH": "bold yellow",
    "CRITICAL": "bold red",
}


class PipelineOrchestrator:
    """Main pipeline runner that sequences all investigation modules.

    Each module receives the :class:`WholeMoneyTrail` plus the output of all
    preceding modules. After all modules complete, alerts are deduplicated by
    content and sorted by :class:`RiskLevel` descending.
    """

    def __init__(self) -> None:
        self.console = console

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def run(self, date: str | None = None) -> dict[str, Any]:
        """Execute the full pipeline for the given investigation date.

        Args:
            date: Investigation date in 'YYYY-MM-DD' format. Defaults to today.

        Returns:
            Dict containing:
                - ``trail``: The :class:`WholeMoneyTrail` snapshot.
                - ``reports``: Dict of module_name → :class:`PipelineReport`.
                - ``all_alerts``: Deduplicated, prioritised list of all alerts.
                - ``summary``: High-level statistics dict.
                - ``elapsed_seconds``: Total pipeline run time.
        """
        run_date = date or datetime.utcnow().strftime("%Y-%m-%d")
        start_time = time.time()

        self._print_pipeline_header(run_date)

        reports: dict[str, PipelineReport] = {}
        trail: WholeMoneyTrail | None = None

        # ── Module 1: Briefing ────────────────────────────────────────────
        trail, reports["BRIEFING"] = self._run_module(
            label="[1/5] BRIEFING",
            description="Carregando Money Trail e gerando alertas iniciais",
            fn=self._run_briefing,
            args=(run_date,),
        )

        # ── Module 2: System Health Check ─────────────────────────────────
        _, reports["SYSTEM_HEALTH_CHECK"] = self._run_module(
            label="[2/5] SYSTEM HEALTH CHECK",
            description="Verificando APIs e detectando anomalias de dados",
            fn=self._run_health_check,
            args=(trail,),
        )

        # ── Module 3: Dependency Check ────────────────────────────────────
        _, reports["DEPENDENCY_CHECK"] = self._run_module(
            label="[3/5] DEPENDENCY CHECK",
            description="Analisando criação de FIPs, side-pockets e consistência temporal",
            fn=self._run_dependency_check,
            args=(trail,),
        )

        # ── Module 4: Flaky Tracker ───────────────────────────────────────
        _, reports["FLAKY_TRACKER"] = self._run_module(
            label="[4/5] FLAKY TRACKER",
            description="Rastreando padrões de flakiness e esvaziamentos pré-ordem",
            fn=self._run_flaky_tracker,
            args=(trail,),
        )

        # ── Module 5: PR Review Digest ────────────────────────────────────
        prior_reports = list(reports.values())
        _, reports["PR_REVIEW_DIGEST"] = self._run_module(
            label="[5/5] PR REVIEW DIGEST",
            description="Consolidando achados e gerando relatórios CLO/COAF",
            fn=self._run_pr_review_digest,
            args=(trail, prior_reports),
        )

        # ── Post-processing ───────────────────────────────────────────────
        all_alerts = self._collect_and_deduplicate_alerts(reports)
        summary = self._build_summary(trail, reports, all_alerts, run_date)
        elapsed = time.time() - start_time

        self._print_pipeline_summary(summary, all_alerts, elapsed)

        return {
            "trail": trail,
            "reports": reports,
            "all_alerts": all_alerts,
            "summary": summary,
            "elapsed_seconds": elapsed,
        }

    # ------------------------------------------------------------------ #
    # Module runners                                                        #
    # ------------------------------------------------------------------ #

    def _run_briefing(
        self, run_date: str
    ) -> tuple[WholeMoneyTrail, PipelineReport]:
        module = BriefingModule()
        return module.run(run_date)

    def _run_health_check(
        self, trail: WholeMoneyTrail
    ) -> tuple[WholeMoneyTrail, PipelineReport]:
        report = SystemHealthCheck().run(trail)
        return trail, report

    def _run_dependency_check(
        self, trail: WholeMoneyTrail
    ) -> tuple[WholeMoneyTrail, PipelineReport]:
        report = DependencyCheckModule().run(trail)
        return trail, report

    def _run_flaky_tracker(
        self, trail: WholeMoneyTrail
    ) -> tuple[WholeMoneyTrail, PipelineReport]:
        report = FlakyTestTracker().run(trail)
        return trail, report

    def _run_pr_review_digest(
        self,
        trail: WholeMoneyTrail,
        prior_reports: list[PipelineReport],
    ) -> tuple[WholeMoneyTrail, PipelineReport]:
        report = PRReviewDigest().run(trail, prior_reports)
        return trail, report

    # ------------------------------------------------------------------ #
    # Orchestration helpers                                                #
    # ------------------------------------------------------------------ #

    def _run_module(
        self,
        label: str,
        description: str,
        fn: Any,
        args: tuple,
    ) -> tuple[Any, PipelineReport]:
        """Run a single module, printing status before/after execution."""
        self.console.print(f"\n  [bold cyan]{label}[/bold cyan]  {description}")
        t0 = time.time()
        result = fn(*args)
        elapsed_ms = (time.time() - t0) * 1000

        # result is always (trail, PipelineReport)
        trail_or_none, report = result
        status_style = _STATUS_STYLE.get(report.status, "white")
        alert_count = len(report.alerts)
        self.console.print(
            f"    → Status: [{status_style}]{report.status.upper()}[/{status_style}]"
            f"  |  Alertas: [bold]{alert_count}[/bold]"
            f"  |  {elapsed_ms:.0f}ms"
        )
        return trail_or_none, report

    def _collect_and_deduplicate_alerts(
        self, reports: dict[str, PipelineReport]
    ) -> list[Alert]:
        """Collect all alerts, deduplicate by (category, institution, description[:60]),
        and sort by RiskLevel descending."""
        seen: set[tuple] = set()
        unique: list[Alert] = []

        for report in reports.values():
            for alert in report.alerts:
                key = (alert.category, alert.institution, alert.description[:60])
                if key not in seen:
                    seen.add(key)
                    unique.append(alert)

        return sorted(unique, key=lambda a: a.level.value, reverse=True)

    def _build_summary(
        self,
        trail: WholeMoneyTrail,
        reports: dict[str, PipelineReport],
        all_alerts: list[Alert],
        run_date: str,
    ) -> dict[str, Any]:
        """Build the high-level summary dict."""
        by_level: dict[str, int] = {lvl.name: 0 for lvl in RiskLevel}
        for alert in all_alerts:
            by_level[alert.level.name] += 1

        overall = (
            "critical" if by_level["CRITICAL"] > 0
            else "warning" if by_level["HIGH"] > 0
            else "ok"
        )

        return {
            "run_date": run_date,
            "overall_status": overall,
            "total_assets": len(trail.assets),
            "total_institutions": len(trail.institutions),
            "total_tracked_brl": str(trail.total_tracked),
            "total_blocked_brl": str(trail.total_blocked),
            "total_evaded_brl": str(trail.total_evaded),
            "total_unique_alerts": len(all_alerts),
            "alerts_by_level": by_level,
            "module_statuses": {name: r.status for name, r in reports.items()},
        }

    # ------------------------------------------------------------------ #
    # Terminal output                                                       #
    # ------------------------------------------------------------------ #

    def _print_pipeline_header(self, run_date: str) -> None:
        """Print the pipeline ASCII header."""
        header_text = Text()
        header_text.append(f"\n  {PIPELINE_NAME} v{PIPELINE_VERSION}\n", style="bold white")
        header_text.append(f"  Data de Investigação: {run_date}\n", style="cyan")
        header_text.append(
            "\n"
            "  ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐\n"
            "  │  BRIEFING   │──▶│ SYSTEM HEALTH│──▶│ DEPENDENCY CHECK │\n"
            "  └─────────────┘   └──────────────┘   └──────────────────┘\n"
            "                                                │\n"
            "                                                ▼\n"
            "                         ┌──────────────────────────────────┐\n"
            "                         │  FLAKY TRACKER → PR REVIEW DIGEST │\n"
            "                         └──────────────────────────────────┘\n",
            style="dim white",
        )
        self.console.print(
            Panel(header_text, border_style="bold blue", expand=False)
        )

    def _print_pipeline_summary(
        self,
        summary: dict[str, Any],
        all_alerts: list[Alert],
        elapsed: float,
    ) -> None:
        """Print final pipeline summary table."""
        self.console.print("\n")

        # Overall status panel
        overall = summary["overall_status"]
        style = _STATUS_STYLE.get(overall, "white")
        self.console.print(
            Panel(
                f"  Status Geral: [{style}]{overall.upper()}[/{style}]\n"
                f"  Ativos Rastreados: [bold]{summary['total_assets']}[/bold]\n"
                f"  Instituições: [bold]{summary['total_institutions']}[/bold]\n"
                f"  Valor Total Rastreado: [bold]R$ {Decimal(summary['total_tracked_brl']):,.2f}[/bold]\n"
                f"  Valor Evadido Estimado: [bold red]R$ {Decimal(summary['total_evaded_brl']):,.2f}[/bold red]\n"
                f"  Total de Alertas Únicos: [bold]{summary['total_unique_alerts']}[/bold]\n"
                f"  Tempo Total: [bold]{elapsed:.2f}s[/bold]",
                title="[bold]PIPELINE CONCLUÍDO[/bold]",
                border_style=style,
            )
        )

        # Alert breakdown table
        table = Table(title="Alertas por Nível de Risco", border_style="dim")
        table.add_column("Nível", style="bold")
        table.add_column("Quantidade", justify="right")
        table.add_column("Barra")

        by_level = summary["alerts_by_level"]
        for level_name in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = by_level.get(level_name, 0)
            bar = "█" * min(count, 30)
            style = _RISK_STYLE.get(level_name, "white")
            table.add_row(
                f"[{style}]{level_name}[/{style}]",
                f"[{style}]{count}[/{style}]",
                f"[{style}]{bar}[/{style}]",
            )
        self.console.print(table)

        # Top alerts
        if all_alerts:
            alert_table = Table(title="Top Alertas (por Criticidade)", border_style="dim")
            alert_table.add_column("Nível", style="bold", width=10)
            alert_table.add_column("Categoria", width=35)
            alert_table.add_column("Instituição", width=20)
            alert_table.add_column("Descrição (resumo)", width=60)

            for alert in all_alerts[:10]:
                style = _RISK_STYLE.get(alert.level.name, "white")
                alert_table.add_row(
                    f"[{style}]{alert.level.name}[/{style}]",
                    alert.category[:35],
                    alert.institution or "—",
                    alert.description[:60] + "…",
                )
            self.console.print(alert_table)
