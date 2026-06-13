#!/usr/bin/env python3
"""
Pipeline Cognitivo Corporativo — Entry point.
Run: python main.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pipeline.core import CognitivePipeline
from reports.generator import ReportGenerator


def main():
    pipeline = CognitivePipeline()
    result = pipeline.run()

    generator = ReportGenerator()
    generator.export_clo_report(result.pr_digest.clo_report)
    generator.export_coaf_draft(result.pr_digest.coaf_mpf_draft)
    generator.export_asset_map(result.pr_digest.penherable_assets)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
