"""Gerador de relatórios jurídicos em formato texto estruturado."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pipeline.config import REPORTS_DIR, LEGAL_FRAMEWORKS, REPORTING_TARGETS
from pipeline.models import PipelineReport, RiskLevel


def generate_report(report: PipelineReport, output_path: Optional[Path] = None) -> str:
    lines = []

    def h1(text: str) -> None:
        lines.append("=" * 70)
        lines.append(f"  {text.upper()}")
        lines.append("=" * 70)

    def h2(text: str) -> None:
        lines.append(f"\n{'─' * 60}")
        lines.append(f"  {text}")
        lines.append(f"{'─' * 60}")

    def section(title: str, items: list[str]) -> None:
        lines.append(f"\n{title}:")
        for item in items:
            lines.append(f"  • {item}")

    lines.append("")
    h1("RELATÓRIO DE INVESTIGAÇÃO PATRIMONIAL")
    lines.append(f"  Data: {report.run_date.strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"  Gerado por: Pipeline Cognitivo Corporativo v1.0")
    lines.append("")

    all_alerts = report.all_alerts
    critical = [a for a in all_alerts if a.level == RiskLevel.CRITICO]
    high = [a for a in all_alerts if a.level == RiskLevel.ALTO]

    h2("1. SUMÁRIO EXECUTIVO")
    lines.append(f"\n  Total de alertas gerados: {len(all_alerts)}")
    lines.append(f"  • Críticos: {len(critical)}")
    lines.append(f"  • Altos:    {len(high)}")
    lines.append(f"  • Módulos executados: {len(report.modules)}")

    if report.modules:
        metrics = report.modules[0].metrics
        total_brl = metrics.get("total_reported_brl", 0)
        if total_brl:
            lines.append(f"\n  Patrimônio total mapeado: R$ {total_brl:,.2f}")

    h2("2. ALERTAS CRÍTICOS")
    if critical:
        for i, alert in enumerate(critical, 1):
            lines.append(f"\n  {i}. [{alert.category}]")
            lines.append(f"     Título: {alert.title}")
            lines.append(f"     Descrição: {alert.description}")
            lines.append(f"     Ação recomendada: {alert.recommended_action}")
            if alert.institution_id:
                lines.append(f"     Instituição: {alert.institution_id}")
            if alert.asset_id:
                lines.append(f"     Ativo: {alert.asset_id}")
    else:
        lines.append("\n  Nenhum alerta crítico identificado.")

    h2("3. RELATÓRIO POR MÓDULO")
    for module in report.modules:
        lines.append(f"\n  [{module.module_name}] Status: {module.status}")
        lines.append(f"  Alertas: {len(module.alerts)} ({module.critical_alert_count} críticos)")
        lines.append(f"  Findings:")
        for finding in module.findings:
            lines.append(f"    • {finding}")

    h2("4. ENQUADRAMENTO JURÍDICO")
    for key, fw in LEGAL_FRAMEWORKS.items():
        lines.append(f"\n  {fw['description']}")
        if "penalty" in fw:
            lines.append(f"    Pena: {fw['penalty']}")
        if "effect" in fw:
            lines.append(f"    Efeito: {fw['effect']}")
        if "reporting_obligation" in fw:
            lines.append(f"    Órgão competente: {fw['reporting_obligation']}")

    h2("5. DESTINATÁRIOS DO RELATÓRIO")
    for key, target in REPORTING_TARGETS.items():
        lines.append(f"  • {key}: {target}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("  FIM DO RELATÓRIO")
    lines.append("=" * 70)
    lines.append("")

    content = "\n".join(lines)

    if output_path is None:
        timestamp = report.run_date.strftime("%Y%m%d_%H%M%S")
        output_path = REPORTS_DIR / f"relatorio_{timestamp}.txt"

    output_path.write_text(content, encoding="utf-8")
    return str(output_path)
