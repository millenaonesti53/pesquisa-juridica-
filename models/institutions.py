from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from .assets import SisbajudCode, SisbajudResponse


class RiskLevel(Enum):
    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class InstitutionStatus(Enum):
    ONLINE = "online"
    DEGRADADO = "degradado"
    OFFLINE = "offline"
    SEM_RESPOSTA = "sem_resposta"


@dataclass
class Institution:
    nome: str
    ispb: str
    tipo: str
    status: InstitutionStatus = InstitutionStatus.ONLINE
    sisbajud_response: Optional[SisbajudResponse] = None
    saldo_atual: Optional[Decimal] = None
    saldo_anterior: Optional[Decimal] = None
    ultima_verificacao: Optional[datetime] = None
    alertas: list[str] = field(default_factory=list)

    @property
    def risco(self) -> RiskLevel:
        if self.status == InstitutionStatus.SEM_RESPOSTA:
            return RiskLevel.CRITICO
        if self.sisbajud_response and self.sisbajud_response.suspeito:
            return RiskLevel.ALTO
        if self._esvaziamento_tatico:
            return RiskLevel.CRITICO
        if self.status == InstitutionStatus.DEGRADADO:
            return RiskLevel.MEDIO
        return RiskLevel.BAIXO

    @property
    def _esvaziamento_tatico(self) -> bool:
        if self.saldo_atual is None or self.saldo_anterior is None:
            return False
        if self.saldo_anterior > Decimal("50000"):
            queda = (self.saldo_anterior - self.saldo_atual) / self.saldo_anterior
            return queda > Decimal("0.90")
        return False

    def adicionar_alerta(self, msg: str) -> None:
        self.alertas.append(f"[{datetime.now().strftime('%H:%M')}] {msg}")

    def avaliar_esvaziamento(self) -> None:
        if self._esvaziamento_tatico:
            self.adicionar_alerta(
                f"ESVAZIAMENTO TÁTICO: R$ {self.saldo_anterior:,.2f} "
                f"→ R$ {self.saldo_atual:,.2f} "
                f"({(1 - self.saldo_atual/self.saldo_anterior)*100:.1f}% de queda)"
            )

    def avaliar_nao_resposta(self) -> None:
        if (
            self.sisbajud_response
            and self.sisbajud_response.codigo == SisbajudCode.NAO_RESPONDEU
        ):
            self.status = InstitutionStatus.SEM_RESPOSTA
            self.adicionar_alerta(
                f"NÃO RESPONDEU ao SISBAJUD — Código 98 — "
                f"prazo expirado sem manifestação"
            )
