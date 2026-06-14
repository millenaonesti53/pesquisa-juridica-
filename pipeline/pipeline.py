"""
Pipeline Cognitivo Corporativo — Orquestrador Principal
Executa os 5 módulos em sequência e consolida o relatório final.
"""

from datetime import datetime, date
from typing import Optional

from pipeline.models import ModuleResult, PipelineReport, RiskLevel
from pipeline.modules import briefing, health_check, dependency_update, flaky_tracker, pr_review_digest


PIPELINE_MODULES = [
    ("BRIEFING", briefing.run),
    ("SYSTEM_HEALTH_CHECK", health_check.run),
    ("DEPENDENCY_UPDATE_CHECK", dependency_update.run),
    ("FLAKY_TEST_TRACKER", flaky_tracker.run),
    ("PR_REVIEW_DIGEST", pr_review_digest.run),
]


def run_pipeline(run_date: Optional[date] = None, verbose: bool = True) -> PipelineReport:
    run_date = run_date or date.today()
    report = PipelineReport(run_date=datetime.now())

    if verbose:
        _print_header(run_date)

    for module_name, module_fn in PIPELINE_MODULES:
        if verbose:
            print(f"\n{'─'*60}")
            print(f"  Executando módulo: {module_name}")
            print(f"{'─'*60}")

        if module_name == "BRIEFING":
            result: ModuleResult = module_fn(run_date)
        else:
            result = module_fn()

        report.modules.append(result)

        if verbose:
            _print_module_result(result)

    if verbose:
        _print_final_summary(report)

    return report


def _print_header(run_date: date) -> None:
    print("\n" + "═" * 70)
    print("  PIPELINE COGNITIVO CORPORATIVO")
    print("  Investigação Patrimonial e Governança Jurídica")
    print(f"  Data de execução: {run_date.strftime('%d/%m/%Y')}")
    print("═" * 70)


def _print_module_result(result: ModuleResult) -> None:
    status_icon = "🔴" if "CRITICO" in result.status else ("🟡" if "ALERTA" in result.status or "DEGRADADO" in result.status else "🟢")
    print(f"\n  {status_icon} Status: {result.status}")
    print(f"  Alertas: {len(result.alerts)} ({result.critical_alert_count} críticos)")
    print()

    for finding in result.findings:
        print(f"    • {finding}")

    if result.alerts:
        critical = [a for a in result.alerts if a.level == RiskLevel.CRITICO]
        if critical:
            print(f"\n  ⚠️  ALERTAS CRÍTICOS ({len(critical)}):")
            for alert in critical:
                print(f"    [{alert.level.value}] {alert.title}")
                print(f"    → {alert.recommended_action}")


def _print_final_summary(report: PipelineReport) -> None:
    all_alerts = report.all_alerts
    critical = [a for a in all_alerts if a.level == RiskLevel.CRITICO]
    high = [a for a in all_alerts if a.level == RiskLevel.ALTO]

    print("\n" + "═" * 70)
    print("  SUMÁRIO EXECUTIVO — PIPELINE COMPLETO")
    print("═" * 70)
    print(f"\n  Módulos executados: {len(report.modules)}")
    print(f"  Total de alertas: {len(all_alerts)}")
    print(f"    • Críticos: {len(critical)}")
    print(f"    • Altos:    {len(high)}")

    if critical:
        print("\n  PRIORIDADES IMEDIATAS:")
        for i, alert in enumerate(critical[:5], 1):
            print(f"  {i}. [{alert.category}] {alert.title}")
            print(f"     → {alert.recommended_action}")

    print("\n" + "═" * 70)
    print("  Pipeline concluído em:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("═" * 70)
