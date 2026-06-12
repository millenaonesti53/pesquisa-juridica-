"""
CVM — Comissão de Valores Mobiliários
Consulta de FIPs, fundos de investimento, PL declarado e alterações de regulamento.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


@dataclass
class CVMFundData:
    cnpj: str
    nome: str
    pl: Decimal
    data_pl: date
    situacao: str
    alteracoes_regulamento: list[dict]
    classes: list[dict]


class CVMClient:
    """
    Cliente para API da CVM (dados.cvm.gov.br).
    Em produção conecta ao endpoint real; aqui usa dados de investigação.
    """

    BASE_URL = "https://dados.cvm.gov.br/dados/FI"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self._cache: dict[str, CVMFundData] = {}

    def consultar_fip(self, cnpj: str) -> Optional[CVMFundData]:
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        if cnpj_limpo in self._cache:
            return self._cache[cnpj_limpo]
        dados = self._dados_investigacao().get(cnpj_limpo)
        if dados:
            self._cache[cnpj_limpo] = dados
        return dados

    def verificar_alteracao_regulamento(
        self, cnpj: str, data_inicio_litigio: date
    ) -> list[dict]:
        dados = self.consultar_fip(cnpj)
        if not dados:
            return []
        return [
            alt for alt in dados.alteracoes_regulamento
            if date.fromisoformat(alt["data"]) >= data_inicio_litigio
        ]

    def detectar_side_pocket(self, cnpj: str) -> bool:
        dados = self.consultar_fip(cnpj)
        if not dados:
            return False
        return any(
            cls.get("tipo") == "side_pocket" or "side" in cls.get("nome", "").lower()
            for cls in dados.classes
        )

    def listar_classes_pos_litigio(
        self, cnpj: str, data_litigio: date
    ) -> list[dict]:
        dados = self.consultar_fip(cnpj)
        if not dados:
            return []
        return [
            cls for cls in dados.classes
            if date.fromisoformat(cls.get("data_criacao", "2000-01-01")) >= data_litigio
        ]

    def verificar_divergencia_pl(
        self, cnpj: str, pl_declarado: Decimal
    ) -> Optional[Decimal]:
        dados = self.consultar_fip(cnpj)
        if not dados:
            return None
        return abs(pl_declarado - dados.pl)

    def _dados_investigacao(self) -> dict[str, CVMFundData]:
        return {
            "40000000000191": CVMFundData(
                cnpj="40.000.000/0001-91",
                nome="FRAM XIV FIP",
                pl=Decimal("3877255.47"),
                data_pl=date(2025, 12, 31),
                situacao="EM FUNCIONAMENTO NORMAL",
                alteracoes_regulamento=[
                    {"data": "2024-03-15", "descricao": "Criação da Classe J — segregação de ativos"},
                    {"data": "2024-07-22", "descricao": "Inclusão de cláusula de side-pocket"},
                ],
                classes=[
                    {"nome": "Classe A", "tipo": "ordinária", "data_criacao": "2019-06-10", "pl": "1200000.00"},
                    {"nome": "Classe J", "tipo": "ordinária", "data_criacao": "2024-03-15", "pl": "950000.00"},
                    {"nome": "Classe Side-Pocket", "tipo": "side_pocket", "data_criacao": "2024-07-22", "pl": "1727255.47"},
                ],
            ),
            "52000000000105": CVMFundData(
                cnpj="52.000.000/0001-05",
                nome="OSLO CAPITAL FIP",
                pl=Decimal("0"),
                data_pl=date(2025, 12, 31),
                situacao="CANCELADO",
                alteracoes_regulamento=[],
                classes=[],
            ),
            "73000000000162": CVMFundData(
                cnpj="73.000.000/0001-62",
                nome="BONIFÁCIO FIP",
                pl=Decimal("8500000.00"),
                data_pl=date(2025, 12, 31),
                situacao="EM FUNCIONAMENTO NORMAL",
                alteracoes_regulamento=[
                    {"data": "2023-11-01", "descricao": "Constituição do fundo"},
                ],
                classes=[
                    {"nome": "Única", "tipo": "ordinária", "data_criacao": "2023-11-01", "pl": "8500000.00"},
                ],
            ),
            "61000000000100": CVMFundData(
                cnpj="61.000.000/0001-00",
                nome="AJACCIO INVESTIMENTOS FIP",
                pl=Decimal("2100000.00"),
                data_pl=date(2024, 6, 30),
                situacao="EM LIQUIDAÇÃO",
                alteracoes_regulamento=[
                    {"data": "2023-05-10", "descricao": "Alteração retroativa de data de constituição"},
                ],
                classes=[
                    {"nome": "Classe I", "tipo": "ordinária", "data_criacao": "2020-01-15", "pl": "2100000.00"},
                ],
            ),
        }
