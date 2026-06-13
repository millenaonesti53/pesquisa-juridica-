"""Asset and financial instrument models."""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class AssetType(str, Enum):
    FIP = "FIP"
    CDB = "CDB"
    LIG = "LIG"
    CONTA_CORRENTE = "CONTA_CORRENTE"
    POUPANCA = "POUPANCA"
    ACAO = "ACAO"
    IMOVEL = "IMOVEL"
    VEICULO = "VEICULO"
    OUTRO = "OUTRO"


class RiskLevel(str, Enum):
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAIXO = "BAIXO"
    MONITORAMENTO = "MONITORAMENTO"


@dataclass
class Asset:
    id: str
    institution: str
    asset_type: AssetType
    description: str
    balance: Decimal
    reference_date: datetime
    sisbajud_code: Optional[int] = None
    previous_balance: Optional[Decimal] = None
    risk_level: RiskLevel = RiskLevel.MONITORAMENTO
    notes: str = ""
    is_penherable: bool = True
    legal_basis_impenhorability: Optional[str] = None

    @property
    def balance_variation(self) -> Optional[Decimal]:
        if self.previous_balance is None or self.previous_balance == 0:
            return None
        return (self.balance - self.previous_balance) / self.previous_balance

    @property
    def is_suspect_drain(self) -> bool:
        variation = self.balance_variation
        if variation is None:
            return False
        return variation < Decimal("-0.80")


@dataclass
class FIP:
    """Fundo de Investimento em Participações."""
    cnpj: str
    name: str
    administrator: str
    pl_current: Decimal
    pl_declared: Decimal
    creation_date: datetime
    last_updated: datetime
    has_side_pocket: bool = False
    has_retroactive_class: bool = False
    classes: list = field(default_factory=list)
    spv_count: int = 0
    notes: str = ""

    @property
    def pl_divergence(self) -> Decimal:
        return abs(self.pl_current - self.pl_declared)

    @property
    def is_suspicious(self) -> bool:
        return (
            self.has_side_pocket
            or self.has_retroactive_class
            or self.pl_divergence > Decimal("100000")
        )
