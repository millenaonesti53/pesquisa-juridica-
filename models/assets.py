from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class SisbajudCode(Enum):
    BLOQUEIO_EFETUADO = "01"
    SALDO_INSUFICIENTE = "02"
    CONTA_ENCERRADA = "03"
    ORDEM_INVALIDA = "04"
    CUMPRIDO_PARCIALMENTE = "05"
    DESBLOQUEIO_EFETUADO = "11"
    RESPONDIDO_SEM_SALDO = "13"
    NAO_RESPONDEU = "98"
    ERRO_SISTEMA = "99"

    @property
    def descricao(self) -> str:
        descricoes = {
            "01": "Bloqueio efetuado com sucesso",
            "02": "Saldo insuficiente para bloqueio integral",
            "03": "Conta encerrada",
            "04": "Ordem inválida ou expirada",
            "05": "Cumprido parcialmente",
            "11": "Desbloqueio efetuado",
            "13": "Respondido sem saldo disponível",
            "98": "Instituição não respondeu — prazo expirado",
            "99": "Erro de sistema — reenvio necessário",
        }
        return descricoes.get(self.value, "Código desconhecido")

    @property
    def risco_ocultacao(self) -> bool:
        return self in (SisbajudCode.NAO_RESPONDEU, SisbajudCode.RESPONDIDO_SEM_SALDO)


@dataclass
class SisbajudResponse:
    instituicao: str
    codigo: SisbajudCode
    valor_bloqueado: Optional[Decimal] = None
    data_resposta: Optional[datetime] = None
    observacao: str = ""

    @property
    def suspeito(self) -> bool:
        return self.codigo.risco_ocultacao


@dataclass
class Asset:
    id: str
    descricao: str
    tipo: str
    valor: Decimal
    instituicao: str
    data_referencia: date
    ativo: bool = True
    penhoravel: bool = True
    observacao: str = ""
    variacao_suspeita: bool = False

    def registrar_variacao(self, valor_anterior: Decimal) -> None:
        if valor_anterior > 0:
            variacao_pct = abs(self.valor - valor_anterior) / valor_anterior * 100
            if variacao_pct > 90 and self.valor < valor_anterior:
                self.variacao_suspeita = True
                self.observacao = (
                    f"Queda de {variacao_pct:.1f}%: "
                    f"R$ {valor_anterior:,.2f} → R$ {self.valor:,.2f}"
                )


@dataclass
class ClasseFIP:
    nome: str
    data_criacao: date
    pl: Decimal
    tipo: str = "ordinária"
    side_pocket: bool = False
    criada_pos_litigio: bool = False
    regulamento_alterado: bool = False

    def risco_estrutural(self) -> list[str]:
        riscos: list[str] = []
        if self.side_pocket:
            riscos.append("Side-pocket identificado — possível segregação indevida de ativos")
        if self.criada_pos_litigio:
            riscos.append("Classe criada após início do litígio — indício de fraude à execução")
        if self.regulamento_alterado:
            riscos.append("Regulamento alterado durante litígio")
        return riscos


@dataclass
class FIP:
    nome: str
    cnpj: str
    administrador: str
    pl_declarado: Decimal
    pl_cvm: Optional[Decimal]
    data_constituicao: date
    classes: list[ClasseFIP] = field(default_factory=list)
    ativo: bool = True

    @property
    def divergencia_pl(self) -> Optional[Decimal]:
        if self.pl_cvm is None:
            return None
        return abs(self.pl_declarado - self.pl_cvm)

    @property
    def tem_divergencia_critica(self) -> bool:
        div = self.divergencia_pl
        if div is None:
            return False
        return div > Decimal("100000")

    def riscos(self) -> list[str]:
        r: list[str] = []
        for cls in self.classes:
            r.extend(cls.risco_estrutural())
        if self.tem_divergencia_critica:
            r.append(
                f"Divergência de PL: declarado R$ {self.pl_declarado:,.2f} "
                f"vs CVM R$ {self.pl_cvm:,.2f}"
            )
        return r
