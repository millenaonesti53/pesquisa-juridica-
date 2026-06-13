"""
Pipeline Cognitivo Corporativo — Orquestrador Principal
Executa os 5 módulos em sequência, cada um alimentando o próximo.
"""
from dataclasses import dataclass
from datetime import datetime
import logging
import sys

from pipeline.modules.briefing import BriefingModule, BriefingReport
from pipeline.modules.health_check import HealthCheckModule, HealthCheckReport
from pipeline.modules.dependency_check import DependencyCheckModule, DependencyReport
from pipeline.modules.flaky_tracker import FlakyTrackerModule, FlakyTrackerReport
from pipeline.modules.pr_digest import PRDigestModule, PRDigestReport

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    started_at: datetime
    finished_at: datetime
    briefing: BriefingReport
    health_check: HealthCheckReport
    dependency_check: DependencyReport
    flaky_tracker: FlakyTrackerReport
    pr_digest: PRDigestReport
    success: bool
    error: str = ""

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    @property
    def has_critical_issues(self) -> bool:
        return (
            bool(self.briefing.critical_alerts)
            or self.health_check.has_critical_issues
            or bool(self.dependency_check.critical_findings)
            or self.flaky_tracker.systematic_concealment_detected
        )


class CognitivePipeline:
    """
    Main orchestrator for the Corporate Cognitive Pipeline.

    Execution order:
      1. Briefing          → Context + daily intelligence
      2. Health Check      → Infrastructure + fraud detection
      3. Dependency Check  → Data freshness + structural anomalies
      4. Flaky Tracker     → Statistical validation + concealment patterns
      5. PR Digest         → Governance + legal instruments
    """

    def __init__(self):
        self.briefing = BriefingModule()
        self.health_check = HealthCheckModule()
        self.dependency_check = DependencyCheckModule()
        self.flaky_tracker = FlakyTrackerModule()
        self.pr_digest = PRDigestModule()

    def run(self) -> PipelineResult:
        started_at = datetime.now()
        logger.info("=" * 60)
        logger.info("PIPELINE COGNITIVO CORPORATIVO — INICIANDO")
        logger.info("=" * 60)

        try:
            # Stage 1: Briefing
            logger.info("[1/5] BRIEFING")
            briefing_result = self.briefing.run()

            # Stage 2: System Health Check
            logger.info("[2/5] SYSTEM HEALTH CHECK")
            health_result = self.health_check.run()

            # Stage 3: Dependency Update Check
            logger.info("[3/5] DEPENDENCY UPDATE CHECK")
            dep_result = self.dependency_check.run()

            # Stage 4: Flaky Test Tracker
            logger.info("[4/5] FLAKY TEST TRACKER")
            flaky_result = self.flaky_tracker.run()

            # Stage 5: PR Review Digest (consumes all upstream outputs)
            logger.info("[5/5] PR REVIEW DIGEST")
            digest_result = self.pr_digest.run(
                briefing=briefing_result,
                health=health_result,
                dependencies=dep_result,
                flaky=flaky_result,
            )

            finished_at = datetime.now()
            result = PipelineResult(
                started_at=started_at,
                finished_at=finished_at,
                briefing=briefing_result,
                health_check=health_result,
                dependency_check=dep_result,
                flaky_tracker=flaky_result,
                pr_digest=digest_result,
                success=True,
            )

            self._print_final_summary(result)
            return result

        except Exception as exc:
            logger.exception(f"Pipeline failed: {exc}")
            raise

    def _print_final_summary(self, result: PipelineResult) -> None:
        logger.info("=" * 60)
        logger.info("PIPELINE CONCLUÍDO")
        logger.info(f"  Duração:              {result.duration_seconds:.2f}s")
        logger.info(f"  Alertas críticos:     {result.pr_digest.critical_alert_count}")
        logger.info(f"  Total recuperável:    R${result.pr_digest.total_recoverable:,.2f}")
        logger.info(f"  Ocultação sistêmica:  {'SIM ⚠️' if result.flaky_tracker.systematic_concealment_detected else 'NÃO'}")
        logger.info(f"  Decisões pendentes:   {len(result.pr_digest.pending_decisions)}")
        logger.info("=" * 60)

        if result.has_critical_issues:
            logger.critical("AÇÃO IMEDIATA REQUERIDA — Ver relatório CLO e minuta COAF/MPF")

        logger.info("\n" + result.pr_digest.clo_report)
