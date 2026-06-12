"""
Gerador de relatórios — saída rica no terminal via Rich.
Consolida toda a análise do pipeline em displays visuais e arquivos de saída.
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from pipeline.briefing import DailyIntelligenceReport
from pipeline.health_check import HealthCheckResult, ComponentStatus
from pipeline.dependency_check import DependencyCheckResult
from pipeline.flaky_tracker import FlakyTrackerResult
from pipeline.pr_review import PRReviewDigest


console = Console()


class ReportGenerator:

    def __init__(self, output_dir: str = "reports/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # BRIEFING
    # ------------------------------------------------------------------ #

    def exibir_briefing(self, report: DailyIntelligenceReport) -> None:
        cor_nivel = {
            "CRÍTICO": "bold red",
            "ALTO": "bold yellow",
            "MÉDIO": "yellow",
            "BAIXO": "green",
        }
        nivel = report.nivel_risco_geral
        cor = cor_nivel.get(nivel, "white")

        console.print(Panel(
            f"[bold]Processo:[/bold] {report.caso}\n"
            f"[bold]Data:[/bold] {report.data}\n"
            f"[bold]Nível de Risco:[/bold] [{cor}]{nivel}[/{cor}]\n"
            f"[bold]Total de Alertas:[/bold] {report.total_alertas}",
            title="🌅 BRIEFING — DAILY INTELLIGENCE REPORT",
            border_style="blue",
        ))

        if report.alertas_criticos:
            self._exibir_alertas(report.alertas_criticos, "CRÍTICOS", "red")
        if report.alertas_altos:
            self._exibir_alertas(report.alertas_altos, "ALTOS", "yellow")

        if report.acoes_imediatas:
            console.print(Panel(
                "\n".join(f"  ⚡ {a}" for a in report.acoes_imediatas),
                title="⚡ AÇÕES IMEDIATAS",
                border_style="red",
            ))

        if report.status_institucional:
            t = Table(title="Status Institucional SISBAJUD", box=box.SIMPLE)
            t.add_column("Instituição", style="cyan")
            t.add_column("Status")
            for inst, status in report.status_institucional.items():
                cor_s = "red" if "98" in status or "13" in status else "green"
                t.add_row(inst, f"[{cor_s}]{status}[/{cor_s}]")
            console.print(t)

    # ------------------------------------------------------------------ #
    # HEALTH CHECK
    # ------------------------------------------------------------------ #

    def exibir_health_check(self, result: HealthCheckResult) -> None:
        console.print(Panel(
            f"[bold]Sistema Estável:[/bold] {'✅ SIM' if result.sistema_estavel else '❌ NÃO'}\n"
            f"[bold]Nível de Risco:[/bold] [bold red]{result.nivel_risco_total}[/bold red]\n"
            f"[bold]Riscos Patrimoniais:[/bold] {len(result.riscos_patrimoniais)}\n"
            f"[bold]Alertas de Ocultação:[/bold] {len(result.alertas_ocultacao)}",
            title="🩺 SYSTEM HEALTH CHECK",
            border_style="yellow",
        ))

        t = Table(title="Componentes do Sistema", box=box.SIMPLE)
        t.add_column("Componente", style="cyan", min_width=35)
        t.add_column("Status")
        t.add_column("Latência")
        t.add_column("Detalhe")

        status_cor = {
            ComponentStatus.OK: "green",
            ComponentStatus.DEGRADADO: "yellow",
            ComponentStatus.OFFLINE: "red",
            ComponentStatus.INDISPONIVEL: "bold red",
        }

        for comp in result.componentes:
            cor = status_cor.get(comp.status, "white")
            lat = f"{comp.latencia_ms}ms" if comp.latencia_ms else "—"
            t.add_row(
                comp.nome,
                f"[{cor}]{comp.status.value}[/{cor}]",
                lat,
                comp.detalhe[:60],
            )
        console.print(t)

        if result.riscos_patrimoniais:
            r_table = Table(title="Riscos Patrimoniais Detectados", box=box.SIMPLE)
            r_table.add_column("Tipo", style="red")
            r_table.add_column("Ativo", style="cyan")
            r_table.add_column("Valor em Risco", justify="right")
            r_table.add_column("Enquadramento")
            for risco in result.riscos_patrimoniais:
                r_table.add_row(
                    risco.tipo_risco,
                    risco.ativo[:40],
                    f"R$ {risco.valor_em_risco:,.2f}",
                    "; ".join(risco.enquadramento_legal[:1]),
                )
            console.print(r_table)

    # ------------------------------------------------------------------ #
    # DEPENDENCY CHECK
    # ------------------------------------------------------------------ #

    def exibir_dependency_check(self, result: DependencyCheckResult) -> None:
        console.print(Panel(
            f"[bold]Bases Atualizadas:[/bold] {len(result.bases_atualizadas)}\n"
            f"[bold]Inconsistências:[/bold] {len(result.inconsistencias)}\n"
            f"[bold]Inconsistências Críticas:[/bold] [bold red]{len(result.criticas)}[/bold red]\n"
            f"[bold]Omissões IRPF:[/bold] {len(result.omissoes_irpf)}\n"
            f"[bold]Divergências FATCA/CRS:[/bold] {len(result.divergencias_fatca)}",
            title="🔄 DEPENDENCY UPDATE CHECK",
            border_style="cyan",
        ))

        if result.criticas:
            t = Table(title="Inconsistências CRÍTICAS", box=box.SIMPLE)
            t.add_column("Tipo", style="red")
            t.add_column("Entidade", style="cyan")
            t.add_column("Descrição")
            t.add_column("Pós-Litígio?")
            for inc in result.criticas:
                t.add_row(
                    inc.tipo,
                    inc.entidade[:30],
                    inc.descricao[:60],
                    "[bold red]SIM[/bold red]" if inc.pos_litigio else "não",
                )
            console.print(t)

    # ------------------------------------------------------------------ #
    # FLAKY TRACKER
    # ------------------------------------------------------------------ #

    def exibir_flaky_tracker(self, result: FlakyTrackerResult) -> None:
        score = result.score_ocultacao_global
        cor_score = "red" if score >= 0.8 else "yellow" if score >= 0.5 else "green"

        console.print(Panel(
            f"[bold]Patterns Detectados:[/bold] {len(result.patterns_detectados)}\n"
            f"[bold]Patterns Críticos:[/bold] [bold red]{len(result.patterns_criticos)}[/bold red]\n"
            f"[bold]Entidades Suspeitas:[/bold] {', '.join(result.entidades_suspeitas)}\n"
            f"[bold]Score de Ocultação:[/bold] [{cor_score}]{score:.0%}[/{cor_score}]",
            title="🧪 FLAKY TEST TRACKER",
            border_style="magenta",
        ))

        if result.patterns_criticos:
            t = Table(title="Patterns Críticos de Ocultação", box=box.SIMPLE)
            t.add_column("Pattern", style="red")
            t.add_column("Entidade", style="cyan")
            t.add_column("Confiança", justify="right")
            t.add_column("Ocorrências", justify="right")
            for p in result.patterns_criticos:
                t.add_row(
                    p.tipo.value,
                    p.entidade[:35],
                    f"{p.score_confianca:.0%}",
                    str(p.ocorrencias),
                )
            console.print(t)

    # ------------------------------------------------------------------ #
    # PR REVIEW DIGEST
    # ------------------------------------------------------------------ #

    def exibir_pr_review(self, digest: PRReviewDigest) -> None:
        console.print(Panel(
            f"[bold]Caso:[/bold] {digest.caso}\n"
            f"[bold]Risco Consolidado:[/bold] [bold red]{digest.nivel_risco_consolidado}[/bold red]\n"
            f"[bold]Frameworks Ativados:[/bold] {len(digest.frameworks_ativados)}\n"
            f"[bold]Ativos Penhoráveis:[/bold] {len(digest.ativos_penhoraveis)}\n"
            f"[bold]Total Penhorável:[/bold] [bold green]R$ {digest.total_penhoravel:,.2f}[/bold green]",
            title="🔍 PR REVIEW DIGEST — CONSOLIDADO JURÍDICO",
            border_style="green",
        ))

        t = Table(title="Mapa de Ativos Penhoráveis", box=box.SIMPLE)
        t.add_column("Pri.", justify="center")
        t.add_column("Ativo", style="cyan")
        t.add_column("Tipo")
        t.add_column("Valor Estimado", justify="right")
        t.add_column("Status")
        for ativo in digest.ativos_por_prioridade:
            cor = "green" if "BLOQUEADO" in ativo.status and "PARCI" not in ativo.status else "yellow"
            t.add_row(
                str(ativo.prioridade),
                ativo.descricao[:40],
                ativo.tipo,
                f"R$ {ativo.valor_estimado:,.2f}",
                f"[{cor}]{ativo.status[:30]}[/{cor}]",
            )
        console.print(t)

        if digest.acoes_prioritarias:
            console.print(Panel(
                "\n".join(digest.acoes_prioritarias),
                title="📋 AÇÕES PRIORITÁRIAS",
                border_style="bold red",
            ))

    # ------------------------------------------------------------------ #
    # SALVAR DOCUMENTOS
    # ------------------------------------------------------------------ #

    def salvar_documentos(self, digest: PRReviewDigest) -> list[str]:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivos: list[str] = []

        docs = {
            f"relatorio_clo_{ts}.txt": digest.relatorio_clo,
            f"minuta_coaf_{ts}.txt": digest.minuta_coaf,
            f"parecer_idpj_{ts}.txt": digest.parecer_idpj,
        }

        for nome, conteudo in docs.items():
            if conteudo:
                caminho = self.output_dir / nome
                caminho.write_text(conteudo, encoding="utf-8")
                arquivos.append(str(caminho))

        return arquivos

    # ------------------------------------------------------------------ #
    # HELPERS
    # ------------------------------------------------------------------ #

    def _exibir_alertas(self, alertas: list, nivel: str, cor: str) -> None:
        linhas = []
        for a in alertas:
            linhas.append(f"[{cor}]▶[/{cor}] {a.mensagem}")
            linhas.append(f"   [dim]↳ Ação: {a.acao_recomendada}[/dim]")
        console.print(Panel(
            "\n".join(linhas),
            title=f"[{cor}]Alertas {nivel}[/{cor}]",
            border_style=cor,
        ))
