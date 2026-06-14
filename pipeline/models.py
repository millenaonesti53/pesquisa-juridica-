"""Modelos de dados para o pipeline de investigação patrimonial."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    CRITICO = "CRÍTICO"
    ALTO = "ALTO"
    MEDIO = "MÉDIO"
    BAIXO = "BAIXO"
    INFORMATIVO = "INFORMATIVO"


class AssetStatus(Enum):
    BLOQUEIO_PENDENTE = "Bloqueio Pendente"
    BLOQUEADO = "Bloqueado"
    ESVAZIADO = "Esvaziado"
    SALDO_ZERO_SUSPEITO = "Saldo Zero Suspeito"
    ESVAZIAMENTO_TATICO = "Esvaziamento Tático"
    NAO_RESPONDEU = "Não Respondeu"
    IMPENHORABILIDADE_ALEGADA = "Impenhorabilidade Alegada"
    INCONSISTENCIA_TEMPORAL = "Inconsistência Temporal"
    SUSPEITO = "Suspeito"
    CONFIRMADO_PENHORAVEL = "Confirmado Penhorável"


class InstitutionType(Enum):
    BANCO = "Banco"
    GESTORA_FIP = "Gestora FIP"
    FIP = "FIP"
    FUNDO = "Fundo"


@dataclass
class SisbajudResponse:
    institution_id: str
    institution_name: str
    code: str
    code_description: str
    timestamp: datetime
    is_critical: bool = False
    risk_flag: Optional[str] = None

    @property
    def is_non_response(self) -> bool:
        return self.code == "98"

    @property
    def is_empty_response(self) -> bool:
        return self.code == "13"


@dataclass
class Asset:
    id: str
    name: str
    asset_type: str
    institution_id: str
    value_brl: Optional[float]
    verified_value_brl: Optional[float]
    status: AssetStatus
    flags: list[str] = field(default_factory=list)
    impenhorability_claim: bool = False
    legal_basis_seizure: Optional[str] = None

    @property
    def value_delta(self) -> Optional[float]:
        if self.value_brl is not None and self.verified_value_brl is not None:
            return self.value_brl - self.verified_value_brl
        return None

    @property
    def has_suspicious_drain(self) -> bool:
        delta = self.value_delta
        if delta is None:
            return False
        return delta > 0 and (delta / self.value_brl) > 0.5


@dataclass
class Institution:
    id: str
    name: str
    institution_type: InstitutionType
    sisbajud_code: str
    status: AssetStatus
    risk_level: RiskLevel
    assets: list[Asset] = field(default_factory=list)
    notes: str = ""
    legal_frameworks: list[str] = field(default_factory=list)

    @property
    def total_reported_value(self) -> float:
        return sum(a.value_brl or 0 for a in self.assets)

    @property
    def total_verified_value(self) -> float:
        return sum(a.verified_value_brl or 0 for a in self.assets)

    @property
    def is_non_responsive(self) -> bool:
        return self.sisbajud_code == "98"


@dataclass
class Alert:
    level: RiskLevel
    category: str
    title: str
    description: str
    institution_id: Optional[str]
    asset_id: Optional[str]
    timestamp: datetime = field(default_factory=datetime.now)
    recommended_action: str = ""

    def to_dict(self) -> dict:
        return {
            "level": self.level.value,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "institution_id": self.institution_id,
            "asset_id": self.asset_id,
            "timestamp": self.timestamp.isoformat(),
            "recommended_action": self.recommended_action,
        }


@dataclass
class ModuleResult:
    module_name: str
    status: str
    alerts: list[Alert] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def critical_alert_count(self) -> int:
        return sum(1 for a in self.alerts if a.level == RiskLevel.CRITICO)

    @property
    def has_critical_alerts(self) -> bool:
        return self.critical_alert_count > 0


@dataclass
class PipelineReport:
    run_date: datetime
    modules: list[ModuleResult] = field(default_factory=list)
    total_assets_brl: float = 0.0
    whole_money_trail: list[Asset] = field(default_factory=list)

    @property
    def all_alerts(self) -> list[Alert]:
        alerts = []
        for module in self.modules:
            alerts.extend(module.alerts)
        return sorted(alerts, key=lambda a: (
            ["CRÍTICO", "ALTO", "MÉDIO", "BAIXO", "INFORMATIVO"].index(a.level.value)
        ))

    @property
    def critical_findings(self) -> list[str]:
        findings = []
        for module in self.modules:
            if module.has_critical_alerts:
                findings.extend(module.findings)
        return findings
