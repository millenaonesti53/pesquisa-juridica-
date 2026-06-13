"""Alert and notification models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AlertType(str, Enum):
    NAO_RESPOSTA = "NAO_RESPOSTA"
    ESVAZIAMENTO_TATICO = "ESVAZIAMENTO_TATICO"
    DIVERGENCIA_PL = "DIVERGENCIA_PL"
    SIDE_POCKET = "SIDE_POCKET"
    CLASSE_RETROATIVA = "CLASSE_RETROATIVA"
    SPV_NOVA = "SPV_NOVA"
    VARIACAO_ABRUPTA = "VARIACAO_ABRUPTA"
    INCONSISTENCIA_IRPF_CVM = "INCONSISTENCIA_IRPF_CVM"


class AlertSeverity(str, Enum):
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    INFORMATIVO = "INFORMATIVO"


@dataclass
class Alert:
    id: str
    alert_type: AlertType
    severity: AlertSeverity
    subject: str
    description: str
    institution: str
    created_at: datetime
    asset_id: Optional[str] = None
    amount_at_risk: Optional[float] = None
    legal_refs: list = field(default_factory=list)
    requires_immediate_action: bool = False
    acknowledged: bool = False
    action_taken: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.alert_type.value,
            "severity": self.severity.value,
            "subject": self.subject,
            "description": self.description,
            "institution": self.institution,
            "created_at": self.created_at.isoformat(),
            "amount_at_risk": self.amount_at_risk,
            "legal_refs": self.legal_refs,
            "requires_immediate_action": self.requires_immediate_action,
        }
