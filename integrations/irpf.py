"""
IRPF — Receita Federal / e-CAC
Consulta de declarações de bens, rendimentos e variação patrimonial para
cruzamento com dados CVM, SISBAJUD e extratos bancários.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class BemIRPF:
    codigo: str
    descricao: str
    valor_ano_anterior: Decimal
    valor_ano_atual: Decimal
    cnpj_instituicao: Optional[str] = None
    informado: bool = True

    @property
    def variacao(self) -> Decimal:
        return self.valor_atual - self.valor_ano_anterior

    @property
    def valor_atual(self) -> Decimal:
        return self.valor_ano_atual

    @property
    def omitido(self) -> bool:
        return not self.informado


@dataclass
class DeclaracaoIRPF:
    cpf: str
    ano_base: int
    bens: list[BemIRPF]
    rendimentos_tributaveis: Decimal
    rendimentos_isentos: Decimal
    data_entrega: Optional[date] = None
    retificada: bool = False

    @property
    def patrimonio_total(self) -> Decimal:
        return sum(b.valor_atual for b in self.bens if not b.omitido)

    @property
    def bens_omitidos(self) -> list[BemIRPF]:
        return [b for b in self.bens if b.omitido]


class IRPFClient:
    """
    Cliente para cruzamento de dados IRPF × CVM × SISBAJUD.
    Detecta omissões, divergências e variação patrimonial injustificada.
    """

    def __init__(self):
        self._declaracoes: dict[str, list[DeclaracaoIRPF]] = self._carregar_dados()

    def consultar_declaracoes(self, cpf: str, anos: list[int]) -> list[DeclaracaoIRPF]:
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        todas = self._declaracoes.get(cpf_limpo, [])
        return [d for d in todas if d.ano_base in anos]

    def detectar_omissoes(self, cpf: str, ativos_cvm: list[dict]) -> list[dict]:
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        declaracoes = self._declaracoes.get(cpf_limpo, [])
        if not declaracoes:
            return []

        ultima = max(declaracoes, key=lambda d: d.ano_base)
        cnpjs_declarados = {
            b.cnpj_instituicao
            for b in ultima.bens
            if b.cnpj_instituicao and b.informado
        }

        omissoes = []
        for ativo in ativos_cvm:
            if ativo.get("cnpj") and ativo["cnpj"] not in cnpjs_declarados:
                omissoes.append({
                    "ativo": ativo.get("nome"),
                    "cnpj": ativo.get("cnpj"),
                    "valor_estimado": ativo.get("pl"),
                    "motivo": "Ativo CVM não declarado no IRPF",
                })
        return omissoes

    def calcular_variacao_patrimonial(
        self, cpf: str, ano_inicio: int, ano_fim: int
    ) -> dict:
        declaracoes = self.consultar_declaracoes(cpf, list(range(ano_inicio, ano_fim + 1)))
        if len(declaracoes) < 2:
            return {"erro": "Dados insuficientes para análise"}

        declaracoes.sort(key=lambda d: d.ano_base)
        primeira = declaracoes[0]
        ultima = declaracoes[-1]

        variacao = ultima.patrimonio_total - primeira.patrimonio_total
        renda_acumulada = sum(
            d.rendimentos_tributaveis + d.rendimentos_isentos for d in declaracoes
        )

        return {
            "patrimonio_inicio": primeira.patrimonio_total,
            "patrimonio_fim": ultima.patrimonio_total,
            "variacao_declarada": variacao,
            "renda_acumulada": renda_acumulada,
            "variacao_injustificada": max(Decimal("0"), variacao - renda_acumulada),
            "anos_analisados": [d.ano_base for d in declaracoes],
        }

    def _carregar_dados(self) -> dict[str, list[DeclaracaoIRPF]]:
        cpf = "12345678901"
        return {
            cpf: [
                DeclaracaoIRPF(
                    cpf=cpf,
                    ano_base=2022,
                    bens=[
                        BemIRPF("71", "Ações e cotas", Decimal("500000"), Decimal("800000")),
                        BemIRPF("99", "Outros bens", Decimal("200000"), Decimal("300000")),
                    ],
                    rendimentos_tributaveis=Decimal("360000"),
                    rendimentos_isentos=Decimal("50000"),
                    data_entrega=date(2023, 4, 28),
                ),
                DeclaracaoIRPF(
                    cpf=cpf,
                    ano_base=2023,
                    bens=[
                        BemIRPF("71", "Ações e cotas", Decimal("800000"), Decimal("820000")),
                        BemIRPF("99", "Outros bens", Decimal("300000"), Decimal("310000")),
                        # FRAM XIV FIP — omitido intencionalmente
                        BemIRPF(
                            "74",
                            "FRAM XIV FIP",
                            Decimal("0"),
                            Decimal("3877255.47"),
                            cnpj_instituicao="40.000.000/0001-91",
                            informado=False,
                        ),
                    ],
                    rendimentos_tributaveis=Decimal("380000"),
                    rendimentos_isentos=Decimal("80000"),
                    data_entrega=date(2024, 4, 26),
                    retificada=False,
                ),
            ]
        }
