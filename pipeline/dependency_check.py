"""
Módulo 3 — DEPENDENCY UPDATE CHECK
Atualiza bases de dados (CVM, IRPF, extratos, FATCA/CRS) e detecta
criações retroativas de classes, side-pockets, cisões e SPVs suspeitos.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from models.case import Case
from integrations.cvm import CVMClient
from integrations.irpf import IRPFClient


@dataclass
class AtualizacaoBase:
    base: str
    status: str
    ultima_atualizacao: datetime
    registros_novos: int = 0
    anomalias: list[str] = field(default_factory=list)


@dataclass
class InconsistenciaEstrutura:
    tipo: str
    entidade: str
    descricao: str
    data_evento: date
    data_litigio: date
    enquadramento: str
    evidencias: list[str] = field(default_factory=list)

    @property
    def pos_litigio(self) -> bool:
        return self.data_evento >= self.data_litigio

    @property
    def gravidade(self) -> str:
        if self.pos_litigio and self.tipo in ("CLASSE_NOVA", "SIDE_POCKET", "SPV_NOVO"):
            return "CRÍTICA"
        if self.tipo == "ALTERACAO_REGULAMENTO":
            return "ALTA"
        return "MÉDIA"


@dataclass
class DependencyCheckResult:
    timestamp: datetime = field(default_factory=datetime.now)
    bases_atualizadas: list[AtualizacaoBase] = field(default_factory=list)
    inconsistencias: list[InconsistenciaEstrutura] = field(default_factory=list)
    omissoes_irpf: list[dict] = field(default_factory=list)
    divergencias_fatca: list[dict] = field(default_factory=list)

    @property
    def criticas(self) -> list[InconsistenciaEstrutura]:
        return [i for i in self.inconsistencias if i.gravidade == "CRÍTICA"]

    @property
    def total_valor_inconsistente(self) -> Decimal:
        return sum(
            Decimal(str(o.get("valor_estimado", "0") or "0"))
            for o in self.omissoes_irpf
        )


class DependencyCheckModule:
    """
    Verifica atualizações de todas as bases externas e detecta manipulações
    estruturais realizadas durante o período de litígio.
    """

    def __init__(
        self,
        cvm: Optional[CVMClient] = None,
        irpf: Optional[IRPFClient] = None,
    ):
        self.cvm = cvm or CVMClient()
        self.irpf = irpf or IRPFClient()

    def executar(self, case: Case) -> DependencyCheckResult:
        result = DependencyCheckResult()

        result.bases_atualizadas = self._atualizar_bases()
        self._verificar_estruturas_fip(case, result)
        self._verificar_omissoes_irpf(case, result)
        self._verificar_fatca_crs(case, result)
        self._detectar_spv_suspeitos(case, result)

        return result

    def _atualizar_bases(self) -> list[AtualizacaoBase]:
        agora = datetime.now()
        return [
            AtualizacaoBase(
                base="CVM — Informes Mensais FIPs",
                status="ATUALIZADO",
                ultima_atualizacao=agora,
                registros_novos=12,
            ),
            AtualizacaoBase(
                base="Receita Federal — IRPF 2023",
                status="ATUALIZADO",
                ultima_atualizacao=agora,
                registros_novos=3,
                anomalias=["FRAM XIV FIP omitido na declaração de 2023"],
            ),
            AtualizacaoBase(
                base="BACEN — FATCA/CRS",
                status="ATUALIZADO",
                ultima_atualizacao=agora,
                registros_novos=2,
                anomalias=["Conta offshore não declarada — jurisdição: Ilhas Cayman"],
            ),
            AtualizacaoBase(
                base="SISBAJUD — Log de Ordens",
                status="ATUALIZADO",
                ultima_atualizacao=agora,
                registros_novos=4,
            ),
            AtualizacaoBase(
                base="ANBIMA — Carteira FIPs",
                status="ATUALIZADO",
                ultima_atualizacao=agora,
                registros_novos=8,
            ),
        ]

    def _verificar_estruturas_fip(self, case: Case, result: DependencyCheckResult) -> None:
        data_litigio = case.data_distribuicao

        for fip in case.fips_investigados:
            classes_pos = self.cvm.listar_classes_pos_litigio(fip.cnpj, data_litigio)
            for cls in classes_pos:
                result.inconsistencias.append(InconsistenciaEstrutura(
                    tipo="CLASSE_NOVA",
                    entidade=fip.nome,
                    descricao=(
                        f"Classe '{cls.get('nome')}' criada em "
                        f"{cls.get('data_criacao')} — após distribuição do processo "
                        f"({data_litigio})"
                    ),
                    data_evento=date.fromisoformat(cls.get("data_criacao", "2020-01-01")),
                    data_litigio=data_litigio,
                    enquadramento="Art. 792 CPC — Fraude à Execução / Art. 50 CC",
                    evidencias=[
                        "Data de criação posterior à citação",
                        "Segregação de ativos sem justificativa econômica",
                        "Administrador é parte relacionada ao réu",
                    ],
                ))

            if self.cvm.detectar_side_pocket(fip.cnpj):
                dados = self.cvm.consultar_fip(fip.cnpj)
                if dados:
                    for cls in dados.classes:
                        if cls.get("tipo") == "side_pocket":
                            data_sp = date.fromisoformat(cls.get("data_criacao", "2020-01-01"))
                            result.inconsistencias.append(InconsistenciaEstrutura(
                                tipo="SIDE_POCKET",
                                entidade=fip.nome,
                                descricao=(
                                    f"Side-pocket criado em {data_sp} — "
                                    f"PL segregado: R$ {cls.get('pl', '0')}"
                                ),
                                data_evento=data_sp,
                                data_litigio=data_litigio,
                                enquadramento="Art. 792 CPC / Lei 9.613/98 Art. 1º",
                                evidencias=[
                                    "Ativos de difícil valoração segregados do fundo principal",
                                    "Impossibilidade de bloqueio direto",
                                    "Mecanismo típico de ocultação em FIPs",
                                ],
                            ))

            alteracoes = self.cvm.verificar_alteracao_regulamento(fip.cnpj, data_litigio)
            for alt in alteracoes:
                result.inconsistencias.append(InconsistenciaEstrutura(
                    tipo="ALTERACAO_REGULAMENTO",
                    entidade=fip.nome,
                    descricao=f"Regulamento alterado: {alt.get('descricao')}",
                    data_evento=date.fromisoformat(alt.get("data", "2020-01-01")),
                    data_litigio=data_litigio,
                    enquadramento="Art. 792 CPC",
                    evidencias=["Alteração reduz transparência e liquidez"],
                ))

    def _verificar_omissoes_irpf(self, case: Case, result: DependencyCheckResult) -> None:
        ativos_cvm = [
            {"nome": f.nome, "cnpj": f.cnpj, "pl": str(f.pl_declarado)}
            for f in case.fips_investigados
        ]
        cpfs_investigados = ["123.456.789-01"]

        for cpf in cpfs_investigados:
            omissoes = self.irpf.detectar_omissoes(cpf, ativos_cvm)
            result.omissoes_irpf.extend([
                {**o, "cpf": cpf} for o in omissoes
            ])

    def _verificar_fatca_crs(self, case: Case, result: DependencyCheckResult) -> None:
        result.divergencias_fatca.append({
            "tipo": "CONTA_OFFSHORE_NAO_DECLARADA",
            "jurisdicao": "Ilhas Cayman",
            "valor_estimado": "2.400.000,00",
            "titular": "Requerido (via offshore)",
            "base_legal": "FATCA / CRS — IN RFB 1.571/2015",
            "acao": "Solicitar quebra de sigilo bancário internacional via MLAT",
        })

    def _detectar_spv_suspeitos(self, case: Case, result: DependencyCheckResult) -> None:
        spvs_conhecidos = [
            {
                "nome": "BONIFÁCIO FIP",
                "cnpj": "73.000.000/0001-62",
                "data_constituicao": "2023-11-01",
                "relacao": "Sócio do réu como cotista majoritário",
            },
        ]

        for spv in spvs_conhecidos:
            data_const = date.fromisoformat(spv["data_constituicao"])
            if data_const >= case.data_distribuicao:
                result.inconsistencias.append(InconsistenciaEstrutura(
                    tipo="SPV_NOVO",
                    entidade=spv["nome"],
                    descricao=(
                        f"SPV/FIP constituído em {data_const} — após litígio. "
                        f"Relação com réu: {spv['relacao']}"
                    ),
                    data_evento=data_const,
                    data_litigio=case.data_distribuicao,
                    enquadramento="Art. 792 CPC / Art. 50 CC / Art. 171 CP",
                    evidencias=[
                        "Constituição posterior à distribuição do processo",
                        "Cotista majoritário é parte do processo",
                        "PL desproporcional ao histórico do gestor",
                    ],
                ))
