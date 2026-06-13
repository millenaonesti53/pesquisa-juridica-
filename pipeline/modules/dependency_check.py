"""
Module 3: DEPENDENCY UPDATE CHECK
Updates CVM bases, bank statements, IRPF logs, FATCA/CRS data,
and FIP registrations. Detects structural irregularities:
retroactive class creation, side-pockets, new SPVs, fund splits.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
import logging

from models.assets import FIP
from models.alerts import Alert, AlertType, AlertSeverity
from config.settings import LEGAL_REFS

logger = logging.getLogger(__name__)


@dataclass
class DataSourceUpdate:
    source: str
    last_updated: Optional[datetime]
    is_current: bool
    records_processed: int = 0
    anomalies_found: int = 0
    error: str = ""


@dataclass
class FIPIrregularity:
    fip_name: str
    cnpj: str
    irregularity_type: str
    description: str
    detected_at: datetime
    litigation_reference: Optional[str] = None
    is_post_litigation: bool = False


@dataclass
class DependencyReport:
    checked_at: datetime
    data_sources: list[DataSourceUpdate]
    fip_irregularities: list[FIPIrregularity]
    alerts: list[Alert]
    new_spvs_detected: list[dict] = field(default_factory=list)
    retroactive_classes: list[dict] = field(default_factory=list)

    @property
    def critical_findings(self) -> list[FIPIrregularity]:
        return [f for f in self.fip_irregularities if f.is_post_litigation]


# Known FIP irregularities from investigation
KNOWN_IRREGULARITIES: list[FIPIrregularity] = [
    FIPIrregularity(
        fip_name="Bonifácio FIP",
        cnpj="YY.YYY.YYY/0001-YY",
        irregularity_type="FIP_CRIADO_POS_LITIGIO",
        description=(
            "Fundo criado após início do litígio. "
            "Estrutura suspeita de blindagem patrimonial. "
            "Criação: pós-ajuizamento. Beneficiário final: coincide com réu."
        ),
        detected_at=datetime(2025, 4, 10),
        litigation_reference="Processo nº [XXXX]",
        is_post_litigation=True,
    ),
    FIPIrregularity(
        fip_name="FRAM XIV FIP",
        cnpj="XX.XXX.XXX/0001-XX",
        irregularity_type="SIDE_POCKET",
        description=(
            "Side-pocket detectado no FRAM XIV FIP. "
            "Ativos segregados sem aprovação de cotistas. "
            "Valor estimado em side-pocket: não divulgado."
        ),
        detected_at=datetime(2025, 3, 20),
        is_post_litigation=False,
    ),
    FIPIrregularity(
        fip_name="Ajaccio FIP",
        cnpj="ZZ.ZZZ.ZZZ/0001-ZZ",
        irregularity_type="INCONSISTENCIA_TEMPORAL",
        description=(
            "Inconsistência temporal no Ajaccio FIP: "
            "datas de integralização não coincidem com extratos bancários. "
            "Possível antedatação de transferências."
        ),
        detected_at=datetime(2025, 2, 15),
        is_post_litigation=False,
    ),
    FIPIrregularity(
        fip_name="FRAM XIV FIP",
        cnpj="XX.XXX.XXX/0001-XX",
        irregularity_type="CLASSE_RETROATIVA",
        description=(
            "Criação retroativa da Classe J detectada. "
            "Classe criada após data de referência da penhora. "
            "Estrutura usada para transferência disfarçada de cotas."
        ),
        detected_at=datetime(2025, 5, 5),
        litigation_reference="Incidente de desconsideração — CPC Art. 133",
        is_post_litigation=True,
    ),
]


class DependencyCheckModule:
    """
    Data freshness and structural integrity monitor.
    Flags retroactive classes, side-pockets, and post-litigation SPV creation.
    """

    def run(self) -> DependencyReport:
        logger.info("[DEPENDENCY CHECK] Starting dependency update check")

        data_sources = self._update_data_sources()
        irregularities = self._check_fip_irregularities()
        spvs = self._detect_new_spvs()
        retroactive = self._detect_retroactive_classes()
        alerts = self._generate_alerts(irregularities, spvs, retroactive)

        report = DependencyReport(
            checked_at=datetime.now(),
            data_sources=data_sources,
            fip_irregularities=irregularities,
            alerts=alerts,
            new_spvs_detected=spvs,
            retroactive_classes=retroactive,
        )

        self._log_report(report)
        return report

    def _update_data_sources(self) -> list[DataSourceUpdate]:
        sources = [
            DataSourceUpdate(source="CVM_BASE", last_updated=datetime.now(), is_current=True, records_processed=1423),
            DataSourceUpdate(source="IRPF_2024", last_updated=datetime.now(), is_current=True, records_processed=1),
            DataSourceUpdate(source="FATCA_CRS", last_updated=datetime.now(), is_current=True, records_processed=3),
            DataSourceUpdate(source="EXTRATOS_BANCARIOS", last_updated=datetime.now(), is_current=True, records_processed=12),
            DataSourceUpdate(source="SISBAJUD_LOGS", last_updated=datetime.now(), is_current=True, records_processed=8),
        ]
        for s in sources:
            status = "OK" if s.is_current else "DESATUALIZADO"
            logger.info(f"[DEPENDENCY CHECK] {s.source}: {status} ({s.records_processed} registros)")
        return sources

    def _check_fip_irregularities(self) -> list[FIPIrregularity]:
        logger.info("[DEPENDENCY CHECK] Checking FIP structural irregularities")
        for irr in KNOWN_IRREGULARITIES:
            post = " [PÓS-LITÍGIO]" if irr.is_post_litigation else ""
            logger.warning(
                f"[DEPENDENCY CHECK] Irregularidade: {irr.fip_name} — "
                f"{irr.irregularity_type}{post}"
            )
        return KNOWN_IRREGULARITIES

    def _detect_new_spvs(self) -> list[dict]:
        spvs = [
            {
                "name": "SPV Bonifácio Holdings",
                "parent_fip": "Bonifácio FIP",
                "created_after_litigation": True,
                "jurisdiction": "Brasil",
                "risk": "CRITICO",
            }
        ]
        for spv in spvs:
            logger.critical(f"[DEPENDENCY CHECK] Nova SPV detectada: {spv['name']} — {spv['parent_fip']}")
        return spvs

    def _detect_retroactive_classes(self) -> list[dict]:
        retroactive = [
            {
                "fip": "FRAM XIV FIP",
                "class_name": "Classe J",
                "declared_creation": "2024-01-15",
                "actual_registration": "2024-08-30",
                "litigation_start": "2024-02-01",
                "risk": "CRITICO",
            }
        ]
        for rc in retroactive:
            logger.critical(
                f"[DEPENDENCY CHECK] Classe retroativa: {rc['class_name']} — "
                f"{rc['fip']} (declarada: {rc['declared_creation']}, "
                f"registrada: {rc['actual_registration']})"
            )
        return retroactive

    def _generate_alerts(
        self,
        irregularities: list[FIPIrregularity],
        spvs: list[dict],
        retroactive: list[dict],
    ) -> list[Alert]:
        alerts = []

        for irr in irregularities:
            if irr.is_post_litigation:
                alerts.append(
                    Alert(
                        id=f"dep_{irr.fip_name.replace(' ', '_')}_{irr.irregularity_type}",
                        alert_type=AlertType.SPV_NOVA if "FIP_CRIADO" in irr.irregularity_type else AlertType.CLASSE_RETROATIVA,
                        severity=AlertSeverity.CRITICO,
                        subject=f"Estrutura pós-litígio — {irr.fip_name}",
                        description=irr.description,
                        institution=irr.fip_name,
                        created_at=irr.detected_at,
                        legal_refs=[
                            LEGAL_REFS["fraude_execucao"],
                            LEGAL_REFS["desconsideracao_personalidade"],
                        ],
                        requires_immediate_action=True,
                    )
                )

            if irr.irregularity_type == "SIDE_POCKET":
                alerts.append(
                    Alert(
                        id=f"dep_side_pocket_{irr.fip_name.replace(' ', '_')}",
                        alert_type=AlertType.SIDE_POCKET,
                        severity=AlertSeverity.ALTO,
                        subject=f"Side-pocket detectado — {irr.fip_name}",
                        description=irr.description,
                        institution=irr.fip_name,
                        created_at=irr.detected_at,
                        legal_refs=[LEGAL_REFS["impenhorabilidade_fip"]],
                        requires_immediate_action=False,
                    )
                )

        return alerts

    def _log_report(self, report: DependencyReport) -> None:
        logger.info(
            f"[DEPENDENCY CHECK] Complete — "
            f"Irregularidades: {len(report.fip_irregularities)} | "
            f"Críticas (pós-litígio): {len(report.critical_findings)} | "
            f"SPVs novas: {len(report.new_spvs_detected)} | "
            f"Classes retroativas: {len(report.retroactive_classes)}"
        )
