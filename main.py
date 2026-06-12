#!/usr/bin/env python3
"""
Pipeline Cognitivo Corporativo — Investigação Patrimonial
Integração: Tecnologia + Governança Jurídica + Investigação Patrimonial
"""
import sys
from rich.console import Console
from rich.rule import Rule
from rich import print as rprint

from fixtures import criar_caso_investigacao
from pipeline import (
    BriefingModule,
    HealthCheckModule,
    DependencyCheckModule,
    FlakyTrackerModule,
    PRReviewModule,
)
from reports import ReportGenerator

console = Console()


def executar_pipeline(salvar: bool = True) -> None:
    console.print(Rule("[bold blue]PIPELINE COGNITIVO CORPORATIVO[/bold blue]"))
    console.print(
        "[dim]Integração: Tecnologia + Governança Jurídica + Investigação Patrimonial[/dim]\n"
    )

    case = criar_caso_investigacao()
    generator = ReportGenerator()

    console.print(f"[bold]Caso:[/bold] {case.numero_processo}")
    console.print(f"[bold]Requerido:[/bold] {case.requerido}")
    console.print(f"[bold]Valor da Causa:[/bold] R$ {case.valor_causa:,.2f}")
    console.print(f"[bold]Cobertura Atual:[/bold] {case.cobertura_execucao:.1f}%\n")

    # ── Módulo 1: Briefing ─────────────────────────────────────────────
    console.print(Rule("[yellow]1/5 — BRIEFING[/yellow]"))
    briefing_result = BriefingModule().executar(case)
    generator.exibir_briefing(briefing_result)

    # ── Módulo 2: Health Check ─────────────────────────────────────────
    console.print(Rule("[yellow]2/5 — SYSTEM HEALTH CHECK[/yellow]"))
    health_result = HealthCheckModule().executar(case)
    generator.exibir_health_check(health_result)

    # ── Módulo 3: Dependency Check ─────────────────────────────────────
    console.print(Rule("[yellow]3/5 — DEPENDENCY UPDATE CHECK[/yellow]"))
    dep_result = DependencyCheckModule().executar(case)
    generator.exibir_dependency_check(dep_result)

    # ── Módulo 4: Flaky Tracker ────────────────────────────────────────
    console.print(Rule("[yellow]4/5 — FLAKY TEST TRACKER[/yellow]"))
    flaky_result = FlakyTrackerModule().executar(case)
    generator.exibir_flaky_tracker(flaky_result)

    # ── Módulo 5: PR Review Digest ─────────────────────────────────────
    console.print(Rule("[yellow]5/5 — PR REVIEW DIGEST[/yellow]"))
    pr_result = PRReviewModule().executar(
        case,
        briefing=briefing_result,
        health=health_result,
        deps=dep_result,
        flaky=flaky_result,
    )
    generator.exibir_pr_review(pr_result)

    # ── Salvar documentos ──────────────────────────────────────────────
    if salvar:
        arquivos = generator.salvar_documentos(pr_result)
        if arquivos:
            console.print(Rule("[green]DOCUMENTOS GERADOS[/green]"))
            for arq in arquivos:
                console.print(f"  📄 {arq}")

    console.print(Rule("[bold green]PIPELINE CONCLUÍDO[/bold green]"))


if __name__ == "__main__":
    salvar = "--save" in sys.argv or "-s" in sys.argv
    executar_pipeline(salvar=salvar)
