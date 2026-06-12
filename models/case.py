from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from .assets import Asset, FIP
from .institutions import Institution


class CaseStatus(Enum):
    INVESTIGACAO = "investigacao"
    BLOQUEIO_PARCIAL = "bloqueio_parcial"
    BLOQUEIO_TOTAL = "bloqueio_total"
    EXECUCAO = "execucao"
    ENCERRADO = "encerrado"


class LegalFramework(Enum):
    FRAUDE_CP171 = "Art. 171 CP — Estelionato"
    FRAUDE_EXECUCAO_CPC792 = "Art. 792 CPC — Fraude à Execução"
    DESCONSIDERACAO_CC50 = "Art. 50 CC — Desconsideração da Personalidade Jurídica"
    LAVAGEM_9613 = "Lei 9.613/98 — Lavagem de Ativos"
    OCULTACAO_PATRIMONIAL = "Ocultação Patrimonial — Crime Continuado"


@dataclass
class WholeMoneyTrail:
    data_referencia: date
    origem: str
    destino: str
    valor: Decimal
    instrumento: str
    suspeito: bool = False
    justificativa_suspeita: str = ""


@dataclass
class Case:
    numero_processo: str
    requerente: str
    requerido: str
    valor_causa: Decimal
    data_distribuicao: date
    status: CaseStatus = CaseStatus.INVESTIGACAO
    frameworks_aplicaveis: list[LegalFramework] = field(default_factory=list)
    ativos_mapeados: list[Asset] = field(default_factory=list)
    fips_investigados: list[FIP] = field(default_factory=list)
    instituicoes: list[Institution] = field(default_factory=list)
    money_trail: list[WholeMoneyTrail] = field(default_factory=list)
    observacoes: list[str] = field(default_factory=list)

    @property
    def total_ativos_mapeados(self) -> Decimal:
        return sum(a.valor for a in self.ativos_mapeados if a.ativo and a.penhoravel)

    @property
    def total_fips(self) -> Decimal:
        return sum(f.pl_declarado for f in self.fips_investigados if f.ativo)

    @property
    def cobertura_execucao(self) -> Decimal:
        if self.valor_causa == 0:
            return Decimal("0")
        total = self.total_ativos_mapeados + self.total_fips
        return total / self.valor_causa * 100

    @property
    def ativos_com_variacao_suspeita(self) -> list[Asset]:
        return [a for a in self.ativos_mapeados if a.variacao_suspeita]

    @property
    def instituicoes_suspeitas(self) -> list[Institution]:
        from .institutions import RiskLevel
        return [
            i for i in self.instituicoes
            if i.risco in (RiskLevel.ALTO, RiskLevel.CRITICO)
        ]

    def adicionar_observacao(self, obs: str) -> None:
        from datetime import datetime
        self.observacoes.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {obs}")
