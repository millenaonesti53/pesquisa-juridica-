"""
SISBAJUD — Sistema de Busca de Ativos do Poder Judiciário
Integração para consulta de bloqueios, respostas bancárias e rastreamento de ordens.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from models.assets import SisbajudCode, SisbajudResponse


@dataclass
class OrdemSisbajud:
    id_ordem: str
    numero_processo: str
    data_envio: datetime
    valor_solicitado: Decimal
    instituicao: str
    resposta: Optional[SisbajudResponse] = None
    tentativas: int = 1

    @property
    def pendente(self) -> bool:
        return self.resposta is None

    @property
    def nao_respondida(self) -> bool:
        return (
            self.resposta is not None
            and self.resposta.codigo == SisbajudCode.NAO_RESPONDEU
        )

    @property
    def suspeita(self) -> bool:
        return self.resposta is not None and self.resposta.suspeito


class SisbajudClient:
    """
    Cliente SISBAJUD para envio e acompanhamento de ordens de bloqueio.
    Simula o gateway do CNJ em ambiente de investigação.
    """

    def __init__(self, certificado_path: Optional[str] = None):
        self.certificado_path = certificado_path
        self._ordens: dict[str, OrdemSisbajud] = self._carregar_ordens_investigacao()

    def consultar_ordem(self, id_ordem: str) -> Optional[OrdemSisbajud]:
        return self._ordens.get(id_ordem)

    def listar_ordens_processo(self, numero_processo: str) -> list[OrdemSisbajud]:
        return [o for o in self._ordens.values() if o.numero_processo == numero_processo]

    def listar_nao_respondidas(self, numero_processo: str) -> list[OrdemSisbajud]:
        return [o for o in self.listar_ordens_processo(numero_processo) if o.nao_respondida]

    def listar_suspeitas(self, numero_processo: str) -> list[OrdemSisbajud]:
        return [o for o in self.listar_ordens_processo(numero_processo) if o.suspeita]

    def gerar_relatorio_nao_cumprimento(self, numero_processo: str) -> dict:
        ordens = self.listar_ordens_processo(numero_processo)
        nao_respondidas = [o for o in ordens if o.nao_respondida]
        suspeitas = [o for o in ordens if o.suspeita and not o.nao_respondida]
        total_solicitado = sum(o.valor_solicitado for o in ordens)
        total_bloqueado = sum(
            o.resposta.valor_bloqueado or Decimal("0")
            for o in ordens
            if o.resposta and o.resposta.valor_bloqueado
        )

        return {
            "processo": numero_processo,
            "total_ordens": len(ordens),
            "nao_respondidas": len(nao_respondidas),
            "suspeitas": len(suspeitas),
            "valor_solicitado": total_solicitado,
            "valor_bloqueado": total_bloqueado,
            "gap_bloqueio": total_solicitado - total_bloqueado,
            "instituicoes_criticas": [o.instituicao for o in nao_respondidas],
        }

    def _carregar_ordens_investigacao(self) -> dict[str, OrdemSisbajud]:
        processo = "0012345-67.2023.8.26.0100"
        return {
            "SBJ-001": OrdemSisbajud(
                id_ordem="SBJ-001",
                numero_processo=processo,
                data_envio=datetime(2024, 1, 10, 9, 0),
                valor_solicitado=Decimal("3877255.47"),
                instituicao="FRAM XIV FIP / Oslo Capital",
                resposta=SisbajudResponse(
                    instituicao="FRAM XIV FIP",
                    codigo=SisbajudCode.NAO_RESPONDEU,
                    observacao="Prazo de 3 dias úteis expirado sem manifestação",
                ),
            ),
            "SBJ-002": OrdemSisbajud(
                id_ordem="SBJ-002",
                numero_processo=processo,
                data_envio=datetime(2024, 1, 10, 9, 5),
                valor_solicitado=Decimal("1250000.00"),
                instituicao="Itaú Unibanco S.A.",
                resposta=SisbajudResponse(
                    instituicao="Itaú Unibanco S.A.",
                    codigo=SisbajudCode.RESPONDIDO_SEM_SALDO,
                    valor_bloqueado=Decimal("5491.00"),
                    observacao="Saldo residual R$ 5.491 — conta esvaziada antes da ordem",
                ),
            ),
            "SBJ-003": OrdemSisbajud(
                id_ordem="SBJ-003",
                numero_processo=processo,
                data_envio=datetime(2024, 1, 10, 9, 10),
                valor_solicitado=Decimal("650758.60"),
                instituicao="BTG Pactual S.A.",
                resposta=SisbajudResponse(
                    instituicao="BTG Pactual S.A.",
                    codigo=SisbajudCode.RESPONDIDO_SEM_SALDO,
                    valor_bloqueado=Decimal("0"),
                    observacao="Saldo zero — histórico de movimentações anteriores identificado",
                ),
            ),
            "SBJ-004": OrdemSisbajud(
                id_ordem="SBJ-004",
                numero_processo=processo,
                data_envio=datetime(2024, 1, 10, 9, 15),
                valor_solicitado=Decimal("1250000.00"),
                instituicao="Itaú Unibanco S.A. — LIG",
                resposta=SisbajudResponse(
                    instituicao="Itaú Unibanco S.A.",
                    codigo=SisbajudCode.NAO_RESPONDEU,
                    observacao="LIG não reportada ao SISBAJUD",
                ),
            ),
        }
