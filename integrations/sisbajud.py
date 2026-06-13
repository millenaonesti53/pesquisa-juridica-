"""SISBAJUD integration for judicial asset blocking queries."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import logging

from config.settings import (
    SISBAJUD_CODE_NO_RESPONSE,
    SISBAJUD_CODE_NO_BALANCE,
    SISBAJUD_CODE_BALANCE_FOUND,
)
from models.institutions import SisbajudQuery, ResponseStatus, SISBAJUD_STATUS_MAP

logger = logging.getLogger(__name__)


@dataclass
class SisbajudResult:
    query_id: str
    institution: str
    cpf_cnpj: str
    response_code: int
    balance: float
    blocked_amount: float
    queried_at: datetime
    responded_at: Optional[datetime]

    @property
    def status(self) -> ResponseStatus:
        return SISBAJUD_STATUS_MAP.get(self.response_code, ResponseStatus.ERRO_TECNICO)

    @property
    def did_not_respond(self) -> bool:
        return self.response_code == SISBAJUD_CODE_NO_RESPONSE

    @property
    def no_balance_found(self) -> bool:
        return self.response_code == SISBAJUD_CODE_NO_BALANCE


class SisbajudClient:
    """
    Integration layer for SISBAJUD (Sistema de Busca de Ativos do Poder Judiciário).
    Requires PJe credentials and court authorization.
    """

    def __init__(self, court_id: str, process_number: str):
        self.court_id = court_id
        self.process_number = process_number
        self._auth_token: Optional[str] = None

    def authenticate(self, certificate_path: str, password: str) -> bool:
        """Authenticate via digital certificate for PJe access."""
        logger.info(f"Authenticating SISBAJUD for court {self.court_id}")
        return False  # Requires live certificate in production

    def query_institution(
        self, institution_code: str, cpf_cnpj: str
    ) -> Optional[SisbajudResult]:
        """Send BACENJUD/SISBAJUD order to a financial institution."""
        logger.info(
            f"Querying institution {institution_code} for CPF/CNPJ {cpf_cnpj[:4]}***"
        )
        return None

    def bulk_query(
        self, institutions: list[str], cpf_cnpj: str
    ) -> list[SisbajudResult]:
        """Send simultaneous SISBAJUD queries to multiple institutions."""
        results = []
        for inst in institutions:
            result = self.query_institution(inst, cpf_cnpj)
            if result:
                results.append(result)
        return results

    def get_pending_responses(self) -> list[SisbajudQuery]:
        """Retrieve queries awaiting institution response (code 98 candidates)."""
        logger.info("Fetching pending SISBAJUD responses")
        return []

    def classify_non_responses(
        self, queries: list[SisbajudQuery], threshold_hours: float = 72.0
    ) -> list[SisbajudQuery]:
        """Flag queries exceeding threshold without response as code 98."""
        now = datetime.now()
        non_responsive = []
        for q in queries:
            if q.responded_at is None:
                elapsed = (now - q.queried_at).total_seconds() / 3600
                if elapsed > threshold_hours:
                    q.response_code = SISBAJUD_CODE_NO_RESPONSE
                    non_responsive.append(q)
        return non_responsive
