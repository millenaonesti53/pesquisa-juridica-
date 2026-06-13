"""Institution and response tracking models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ResponseStatus(str, Enum):
    RESPONDEU_COM_SALDO = "RESPONDEU_COM_SALDO"
    RESPONDEU_SEM_SALDO = "RESPONDEU_SEM_SALDO"
    NAO_RESPONDEU = "NAO_RESPONDEU"
    BLOQUEADO = "BLOQUEADO"
    ERRO_TECNICO = "ERRO_TECNICO"


SISBAJUD_STATUS_MAP = {
    1: ResponseStatus.RESPONDEU_COM_SALDO,
    2: ResponseStatus.BLOQUEADO,
    13: ResponseStatus.RESPONDEU_SEM_SALDO,
    98: ResponseStatus.NAO_RESPONDEU,
}


@dataclass
class Institution:
    code: str
    name: str
    sisbajud_code: Optional[int]
    response_status: ResponseStatus
    last_queried: datetime
    response_count: int = 0
    no_response_streak: int = 0
    alert_sent: bool = False
    notes: str = ""

    @property
    def is_non_responsive(self) -> bool:
        return self.response_status == ResponseStatus.NAO_RESPONDEU

    @property
    def requires_escalation(self) -> bool:
        return self.no_response_streak >= 3


@dataclass
class SisbajudQuery:
    query_id: str
    institution_code: str
    cpf_cnpj: str
    queried_at: datetime
    response_code: Optional[int] = None
    responded_at: Optional[datetime] = None
    balance_found: bool = False
    amount: float = 0.0

    @property
    def response_latency_hours(self) -> Optional[float]:
        if self.responded_at is None:
            return None
        delta = self.responded_at - self.queried_at
        return delta.total_seconds() / 3600
