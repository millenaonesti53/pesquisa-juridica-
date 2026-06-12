"""
Corporate Cognitive Pipeline — Main Entrypoint.

CLI usage::

    # Run full pipeline (today's date, output to ./output/)
    python main.py

    # Run for a specific date
    python main.py --date 2024-01-15

    # Run only a single module
    python main.py --module briefing

    # Custom output directory
    python main.py --output-dir /tmp/reports

    # Save JSON report
    python main.py --json

Available modules (--module):
    briefing, health_check, dependency_check, flaky_tracker, pr_review_digest
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console

from config.settings import DEFAULT_OUTPUT_DIR, PIPELINE_NAME, PIPELINE_VERSION
from pipeline.orchestrator import PipelineOrchestrator
from pipeline.modules.briefing import BriefingModule
from pipeline.modules.health_check import SystemHealthCheck
from pipeline.modules.dependency_check import DependencyCheckModule
from pipeline.modules.flaky_tracker import FlakyTestTracker
from pipeline.modules.pr_review_digest import PRReviewDigest
from pipeline.reports.generator import ReportGenerator

console = Console()

_SINGLE_MODULES = {
    "briefing": BriefingModule,
    "health_check": SystemHealthCheck,
    "dependency_check": DependencyCheckModule,
    "flaky_tracker": FlakyTestTracker,
    "pr_review_digest": PRReviewDigest,
}


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--date",
    "-d",
    default=None,
    metavar="YYYY-MM-DD",
    help="Investigation date (default: today).",
)
@click.option(
    "--module",
    "-m",
    default=None,
    type=click.Choice(list(_SINGLE_MODULES.keys()), case_sensitive=False),
    help="Run a single module instead of the full pipeline.",
)
@click.option(
    "--output-dir",
    "-o",
    default=DEFAULT_OUTPUT_DIR,
    show_default=True,
    help="Directory for report output files.",
)
@click.option(
    "--json",
    "save_json",
    is_flag=True,
    default=False,
    help="Save a JSON report to the output directory.",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    default=False,
    help="Suppress rich terminal output (useful for CI).",
)
def main(
    date: str | None,
    module: str | None,
    output_dir: str,
    save_json: bool,
    quiet: bool,
) -> None:
    """Corporate Cognitive Pipeline — Patrimonial/Legal Investigation System.

    Runs the full investigation pipeline across all five modules:
    BRIEFING → SYSTEM_HEALTH_CHECK → DEPENDENCY_CHECK → FLAKY_TRACKER
    → PR_REVIEW_DIGEST.

    Each module analyses the money trail from a different angle and
    generates domain-specific legal alerts and recommendations.
    """
    run_date = date or datetime.utcnow().strftime("%Y-%m-%d")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not quiet:
        console.print(
            f"\n[bold blue]{PIPELINE_NAME} v{PIPELINE_VERSION}[/bold blue]\n"
        )

    # ── Single-module mode ────────────────────────────────────────────────
    if module:
        _run_single_module(module, run_date, quiet)
        return

    # ── Full pipeline mode ────────────────────────────────────────────────
    orchestrator = PipelineOrchestrator()

    if quiet:
        # Redirect rich output during orchestration
        import io
        from rich.console import Console as RichConsole
        orchestrator.console = RichConsole(file=io.StringIO())

    result = orchestrator.run(run_date)

    gen = ReportGenerator()
    executive_summary = gen.generate_executive_summary(result)
    full_report = gen.generate_full_report(result)

    # Always save text reports
    _save_text_report(output_path, run_date, "executive_summary", executive_summary)
    _save_text_report(output_path, run_date, "full_report", full_report)

    if save_json:
        json_path = str(output_path / f"pipeline_{run_date}.json")
        gen.export_json(result, json_path)
        if not quiet:
            console.print(f"\n[green]JSON exportado:[/green] {json_path}")

    if not quiet:
        console.print(f"\n[green]Relatórios salvos em:[/green] {output_path.resolve()}")

        # Print executive summary to terminal
        console.rule("[bold]SUMÁRIO EXECUTIVO[/bold]")
        console.print(executive_summary)

    # Exit with non-zero code if pipeline is critical
    if result["summary"]["overall_status"] == "critical":
        sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_single_module(module_name: str, run_date: str, quiet: bool) -> None:
    """Run a single pipeline module in isolation."""
    console.print(f"[bold cyan]Executando módulo: {module_name.upper()}[/bold cyan]\n")

    # All single-module runs need the money trail first
    trail, briefing_report = BriefingModule().run(run_date)

    if module_name == "briefing":
        console.print(f"Status: [bold]{briefing_report.status.upper()}[/bold]")
        console.print(f"Alertas: {len(briefing_report.alerts)}")
        _print_alerts(briefing_report.alerts)
        return

    module_cls = _SINGLE_MODULES[module_name]

    if module_name == "pr_review_digest":
        # PR Review needs prior reports
        hc_report = SystemHealthCheck().run(trail)
        dc_report = DependencyCheckModule().run(trail)
        ft_report = FlakyTestTracker().run(trail)
        report = module_cls().run(trail, [briefing_report, hc_report, dc_report, ft_report])
    else:
        report = module_cls().run(trail)

    console.print(f"Status: [bold]{report.status.upper()}[/bold]")
    console.print(f"Alertas: {len(report.alerts)}")
    _print_alerts(report.alerts)


def _print_alerts(alerts: list) -> None:
    """Print a list of alerts to the console."""
    from pipeline.models import RiskLevel
    for alert in sorted(alerts, key=lambda a: a.level.value, reverse=True):
        style = {
            RiskLevel.CRITICAL: "bold red",
            RiskLevel.HIGH: "bold yellow",
            RiskLevel.MEDIUM: "yellow",
            RiskLevel.LOW: "dim white",
        }.get(alert.level, "white")
        console.print(
            f"  [{style}][{alert.level.name}][/{style}] "
            f"[cyan]{alert.category}[/cyan]: {alert.description[:120]}"
        )


def _save_text_report(
    output_path: Path, run_date: str, report_type: str, content: str
) -> None:
    """Write a text report to disk."""
    filename = f"{report_type}_{run_date}.txt"
    file_path = output_path / filename
    file_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
