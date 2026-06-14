#!/usr/bin/env python3
"""
Pipeline Cognitivo Corporativo — Ponto de entrada principal.

Uso:
    python main.py                    # Executa pipeline completo
    python main.py --report           # Gera relatório em arquivo
    python main.py --quiet            # Execução silenciosa
"""

import argparse
import sys
from datetime import date

from pipeline.pipeline import run_pipeline
from pipeline.report_generator import generate_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pipeline Cognitivo Corporativo — Investigação Patrimonial"
    )
    parser.add_argument("--report", action="store_true", help="Gerar relatório em arquivo")
    parser.add_argument("--quiet", action="store_true", help="Execução sem saída no terminal")
    parser.add_argument("--date", type=str, default=None, help="Data da execução (YYYY-MM-DD)")
    args = parser.parse_args()

    run_date = date.today()
    if args.date:
        try:
            run_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"Erro: data inválida '{args.date}'. Use o formato YYYY-MM-DD.")
            return 1

    report = run_pipeline(run_date=run_date, verbose=not args.quiet)

    if args.report:
        output_path = generate_report(report)
        print(f"\nRelatório gerado em: {output_path}")

    all_alerts = report.all_alerts
    critical_count = sum(1 for a in all_alerts if a.level.value == "CRÍTICO")

    return 1 if critical_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
