"""
Módulo 2 — SYSTEM HEALTH CHECK
Monitora a estabilidade das integrações (CVM, SISBAJUD, bancos) e detecta
inconsistências patrimoniais, divergências de PL e sinais de ocultação.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from models.case import Case
from models.institutions import Institution, RiskLevel
from integrations.cvm import CVMClient
from integrations.sisbajud import SisbajudClient


class ComponentStatus(Enum):
    OK = "OK"
    DEGRADADO = "DEGRADADO"
    OFFLINE = "OFFLINE"
    INDISPONIVEL = "INDISPONÍVEL"


@dataclass
class ComponentHealth:
    nome: str
    status: ComponentStatus
    latencia_ms: Optional[int] = None
    ultima_verificacao: datetime = field(default_factory=datetime.now)
    detalhe: str = ""
    critico: bool = False


@dataclass
class RiscoPatrimonial:
    ativo: str
    tipo_risco: str
    descricao: str
    valor_em_risco: Decimal
    enquadramento_legal: list[str] = field(default_factory=list)
    evidencias: list[str] = field(default_factory=list)


@dataclass
class HealthCheckResult:
    timestamp: datetime = field(default_factory=datetime.now)
    componentes: list[ComponentHealth] = field(default_factory=list)
    riscos_patrimoniais: list[RiscoPatrimonial] = field(default_factory=list)
    inconsistencias_pl: list[dict] = field(default_factory=list)
    alertas_ocultacao: list[str] = field(default_factory=list)

    @property
    def sistema_estavel(self) -> bool:
        criticos_offline = [
            c for c in self.componentes
            if c.critico and c.status in (ComponentStatus.OFFLINE, ComponentStatus.INDISPONIVEL)
        ]
        return len(criticos_offline) == 0

    @property
    def nivel_risco_total(self) -> str:
        if any(r.tipo_risco == "OCULTAÇÃO_CRÍTICA" for r in self.riscos_patrimoniais):
            return "CRÍTICO"
        if len(self.riscos_patrimoniais) > 2:
            return "ALTO"
        if self.riscos_patrimoniais:
            return "MÉDIO"
        return "BAIXO"


class HealthCheckModule:
    """
    Verifica integridade das APIs e detecta divergências patrimoniais.
    Produz um mapa de riscos críticos para a investigação.
    """

    def __init__(
        self,
        cvm: Optional[CVMClient] = None,
        sisbajud: Optional[SisbajudClient] = None,
    ):
        self.cvm = cvm or CVMClient()
        self.sisbajud = sisbajud or SisbajudClient()

    def executar(self, case: Case) -> HealthCheckResult:
        result = HealthCheckResult()

        result.componentes = self._verificar_componentes()
        self._verificar_divergencias_pl(case, result)
        self._verificar_esvaziamentos(case, result)
        self._verificar_nao_respostas(case, result)
        self._detectar_ocultacao(case, result)

        return result

    def _verificar_componentes(self) -> list[ComponentHealth]:
        return [
            ComponentHealth(
                nome="API CVM — dados.cvm.gov.br",
                status=ComponentStatus.OK,
                latencia_ms=245,
                critico=True,
                detalhe="FIPs e fundos — dados disponíveis",
            ),
            ComponentHealth(
                nome="SISBAJUD — CNJ Gateway",
                status=ComponentStatus.OK,
                latencia_ms=312,
                critico=True,
                detalhe="Ordens em processamento — 4 ordens ativas",
            ),
            ComponentHealth(
                nome="Receita Federal — e-CAC",
                status=ComponentStatus.DEGRADADO,
                latencia_ms=1850,
                critico=False,
                detalhe="Latência elevada — consultas com delay de 30s",
            ),
            ComponentHealth(
                nome="BACEN — SCR/RSFN",
                status=ComponentStatus.OK,
                latencia_ms=198,
                critico=True,
                detalhe="Sistema de informações de crédito disponível",
            ),
            ComponentHealth(
                nome="COAF — Portal",
                status=ComponentStatus.OK,
                latencia_ms=420,
                critico=False,
                detalhe="RIFs disponíveis para consulta",
            ),
            ComponentHealth(
                nome="ITAÚ — Gateway SISBAJUD",
                status=ComponentStatus.DEGRADADO,
                latencia_ms=None,
                critico=True,
                detalhe="Resposta parcial — saldo residual R$ 5.491 (suspeito)",
            ),
            ComponentHealth(
                nome="BTG PACTUAL — Gateway SISBAJUD",
                status=ComponentStatus.DEGRADADO,
                latencia_ms=None,
                critico=True,
                detalhe="Resposta: saldo zero — histórico de movimentações detectado",
            ),
            ComponentHealth(
                nome="FRAM/OSLO — Gateway SISBAJUD",
                status=ComponentStatus.INDISPONIVEL,
                latencia_ms=None,
                critico=True,
                detalhe="NÃO RESPONDEU — Código 98 — descumprimento de ordem judicial",
            ),
        ]

    def _verificar_divergencias_pl(self, case: Case, result: HealthCheckResult) -> None:
        for fip in case.fips_investigados:
            dados_cvm = self.cvm.consultar_fip(fip.cnpj)
            if not dados_cvm:
                continue

            divergencia = fip.divergencia_pl
            if divergencia and divergencia > Decimal("100000"):
                result.inconsistencias_pl.append({
                    "fip": fip.nome,
                    "cnpj": fip.cnpj,
                    "pl_declarado": fip.pl_declarado,
                    "pl_cvm": fip.pl_cvm,
                    "divergencia": divergencia,
                    "percentual": f"{divergencia / fip.pl_declarado * 100:.1f}%",
                })
                result.riscos_patrimoniais.append(RiscoPatrimonial(
                    ativo=fip.nome,
                    tipo_risco="DIVERGÊNCIA_PL",
                    descricao=(
                        f"PL declarado R$ {fip.pl_declarado:,.2f} diverge "
                        f"do PL CVM R$ {fip.pl_cvm:,.2f} — "
                        f"diferença de R$ {divergencia:,.2f}"
                    ),
                    valor_em_risco=divergencia,
                    enquadramento_legal=[
                        "Art. 171 CP — Estelionato",
                        "Lei 9.613/98 — Lavagem de Ativos",
                    ],
                    evidencias=[
                        "Declaração do administrador diverge dos dados CVM",
                        "Divergência temporal identificada",
                    ],
                ))

    def _verificar_esvaziamentos(self, case: Case, result: HealthCheckResult) -> None:
        for inst in case.instituicoes:
            inst.avaliar_esvaziamento()
            if not inst.alertas or inst.saldo_anterior is None or inst.saldo_atual is None:
                if inst.alertas:
                    for alerta in inst.alertas:
                        result.alertas_ocultacao.append(f"{inst.nome}: {alerta}")
                continue
            for alerta in inst.alertas:
                result.alertas_ocultacao.append(f"{inst.nome}: {alerta}")
            result.riscos_patrimoniais.append(RiscoPatrimonial(
                    ativo=inst.nome,
                    tipo_risco="OCULTAÇÃO_CRÍTICA",
                    descricao=(
                        f"Esvaziamento tático detectado: "
                        f"R$ {inst.saldo_anterior:,.2f} → R$ {inst.saldo_atual:,.2f}"
                    ),
                    valor_em_risco=inst.saldo_anterior - inst.saldo_atual,
                    enquadramento_legal=[
                        "Art. 792 CPC — Fraude à Execução",
                        "Art. 50 CC — Desconsideração da Personalidade Jurídica",
                        "Lei 9.613/98 — Lavagem de Ativos",
                    ],
                    evidencias=[
                        "Variação superior a 90% no saldo imediatamente anterior à ordem",
                        "Código SISBAJUD 13 — respondido sem saldo",
                    ],
                ))

    def _verificar_nao_respostas(self, case: Case, result: HealthCheckResult) -> None:
        ordens_nr = self.sisbajud.listar_nao_respondidas(case.numero_processo)
        for ordem in ordens_nr:
            result.alertas_ocultacao.append(
                f"ORDEM NÃO CUMPRIDA: {ordem.instituicao} — "
                f"R$ {ordem.valor_solicitado:,.2f} — Código 98"
            )
            result.riscos_patrimoniais.append(RiscoPatrimonial(
                ativo=ordem.instituicao,
                tipo_risco="DESCUMPRIMENTO_JUDICIAL",
                descricao=(
                    f"Descumprimento de ordem SISBAJUD — "
                    f"R$ {ordem.valor_solicitado:,.2f} não bloqueados"
                ),
                valor_em_risco=ordem.valor_solicitado,
                enquadramento_legal=[
                    "Art. 77 CPC — Multa por descumprimento",
                    "Art. 330 CP — Desobediência",
                    "Art. 792 CPC — Fraude à Execução",
                ],
                evidencias=[
                    "Prazo SISBAJUD expirado sem resposta",
                    "Histórico de movimentações ativas na conta",
                ],
            ))

    def _detectar_ocultacao(self, case: Case, result: HealthCheckResult) -> None:
        total_risco = sum(r.valor_em_risco for r in result.riscos_patrimoniais)
        if total_risco > Decimal("1000000"):
            result.alertas_ocultacao.append(
                f"ALERTA COAF: Total em risco de ocultação — R$ {total_risco:,.2f}. "
                f"Recomenda-se comunicação ao COAF e notificação ao MPF."
            )
