"""
Módulo 1 — BRIEFING
Agrega inteligência do dia: movimentações, alertas SISBAJUD, status de FIPs,
e gera o daily intelligence report para o CLO e Núcleo de Governança.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from models.case import Case
from models.assets import SisbajudCode
from integrations.sisbajud import SisbajudClient
from integrations.cvm import CVMClient


@dataclass
class IntelligenceAlert:
    nivel: str
    categoria: str
    mensagem: str
    acao_recomendada: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"[{self.nivel}] {self.categoria}: {self.mensagem}"


@dataclass
class DailyIntelligenceReport:
    data: date
    caso: str
    alertas_criticos: list[IntelligenceAlert] = field(default_factory=list)
    alertas_altos: list[IntelligenceAlert] = field(default_factory=list)
    alertas_medios: list[IntelligenceAlert] = field(default_factory=list)
    status_institucional: dict[str, str] = field(default_factory=dict)
    whole_money_trail_resumo: list[str] = field(default_factory=list)
    acoes_imediatas: list[str] = field(default_factory=list)

    @property
    def total_alertas(self) -> int:
        return len(self.alertas_criticos) + len(self.alertas_altos) + len(self.alertas_medios)

    @property
    def nivel_risco_geral(self) -> str:
        if self.alertas_criticos:
            return "CRÍTICO"
        if self.alertas_altos:
            return "ALTO"
        if self.alertas_medios:
            return "MÉDIO"
        return "BAIXO"


class BriefingModule:
    """
    Agrega e consolida toda a inteligência disponível para o início do dia operacional.
    Carrega o Whole Money Trail, atualiza status SISBAJUD e gera alertas automáticos.
    """

    def __init__(
        self,
        sisbajud: Optional[SisbajudClient] = None,
        cvm: Optional[CVMClient] = None,
    ):
        self.sisbajud = sisbajud or SisbajudClient()
        self.cvm = cvm or CVMClient()

    def executar(self, case: Case) -> DailyIntelligenceReport:
        report = DailyIntelligenceReport(
            data=date.today(),
            caso=case.numero_processo,
        )

        self._analisar_sisbajud(case, report)
        self._analisar_fips(case, report)
        self._analisar_ativos(case, report)
        self._carregar_money_trail(case, report)
        self._gerar_acoes_imediatas(report)

        return report

    def _analisar_sisbajud(self, case: Case, report: DailyIntelligenceReport) -> None:
        ordens = self.sisbajud.listar_ordens_processo(case.numero_processo)

        for ordem in ordens:
            if not ordem.resposta:
                continue

            codigo = ordem.resposta.codigo
            inst = ordem.instituicao

            report.status_institucional[inst] = (
                f"Código {codigo.value} — {codigo.descricao}"
            )

            if codigo == SisbajudCode.NAO_RESPONDEU:
                report.alertas_criticos.append(IntelligenceAlert(
                    nivel="CRÍTICO",
                    categoria="SISBAJUD — Não Resposta",
                    mensagem=(
                        f"{inst}: Código 98 — ausência de resposta ao bloqueio "
                        f"de R$ {ordem.valor_solicitado:,.2f}"
                    ),
                    acao_recomendada=(
                        "Peticionar imediatamente pela aplicação de multa por descumprimento "
                        "(Art. 77 CPC) e reenviar ordem com prazo improrrogável de 24h"
                    ),
                ))

            elif codigo == SisbajudCode.RESPONDIDO_SEM_SALDO:
                valor_bloqueado = ordem.resposta.valor_bloqueado or Decimal("0")
                gap = ordem.valor_solicitado - valor_bloqueado
                report.alertas_altos.append(IntelligenceAlert(
                    nivel="ALTO",
                    categoria="SISBAJUD — Esvaziamento Tático",
                    mensagem=(
                        f"{inst}: Código 13 — respondido com saldo insuficiente. "
                        f"Gap de R$ {gap:,.2f} não coberto. "
                        f"Saldo atual: R$ {valor_bloqueado:,.2f}"
                    ),
                    acao_recomendada=(
                        "Solicitar extrato completo dos últimos 90 dias — "
                        "identificar destinatário das transferências pré-bloqueio"
                    ),
                ))

    def _analisar_fips(self, case: Case, report: DailyIntelligenceReport) -> None:
        data_litigio = case.data_distribuicao

        for fip in case.fips_investigados:
            dados_cvm = self.cvm.consultar_fip(fip.cnpj)
            if not dados_cvm:
                report.alertas_medios.append(IntelligenceAlert(
                    nivel="MÉDIO",
                    categoria="CVM — Dado Ausente",
                    mensagem=f"{fip.nome}: sem dados na CVM — possível cancelamento ou CNPJ incorreto",
                    acao_recomendada="Verificar CNPJ junto ao administrador e consultar ANBIMA",
                ))
                continue

            classes_pos = self.cvm.listar_classes_pos_litigio(fip.cnpj, data_litigio)
            if classes_pos:
                report.alertas_criticos.append(IntelligenceAlert(
                    nivel="CRÍTICO",
                    categoria="FIP — Estrutura Fraudulenta",
                    mensagem=(
                        f"{fip.nome}: {len(classes_pos)} classe(s) criada(s) "
                        f"após início do litígio ({data_litigio}): "
                        + ", ".join(c.get("nome", "") for c in classes_pos)
                    ),
                    acao_recomendada=(
                        "Arguir fraude à execução (Art. 792 CPC) e "
                        "requerer desconsideração da personalidade jurídica (Art. 50 CC)"
                    ),
                ))

            if self.cvm.detectar_side_pocket(fip.cnpj):
                report.alertas_criticos.append(IntelligenceAlert(
                    nivel="CRÍTICO",
                    categoria="FIP — Side-Pocket",
                    mensagem=(
                        f"{fip.nome}: side-pocket identificado — "
                        f"ativos segregados indevidamente durante litígio"
                    ),
                    acao_recomendada=(
                        "Requerer laudo pericial sobre os ativos segregados e "
                        "bloqueio preventivo de toda a estrutura do FIP"
                    ),
                ))

    def _analisar_ativos(self, case: Case, report: DailyIntelligenceReport) -> None:
        for ativo in case.ativos_com_variacao_suspeita:
            report.alertas_criticos.append(IntelligenceAlert(
                nivel="CRÍTICO",
                categoria="Ativo — Variação Abrupta",
                mensagem=f"{ativo.descricao} ({ativo.instituicao}): {ativo.observacao}",
                acao_recomendada=(
                    "Solicitar extrato bancário e rastrear destinatário — "
                    "peticionar bloqueio dos valores transferidos"
                ),
            ))

    def _carregar_money_trail(self, case: Case, report: DailyIntelligenceReport) -> None:
        for trail in case.money_trail:
            if trail.suspeito:
                report.whole_money_trail_resumo.append(
                    f"[SUSPEITO] {trail.origem} → {trail.destino}: "
                    f"R$ {trail.valor:,.2f} via {trail.instrumento} "
                    f"({trail.data_referencia}) — {trail.justificativa_suspeita}"
                )
            else:
                report.whole_money_trail_resumo.append(
                    f"{trail.origem} → {trail.destino}: "
                    f"R$ {trail.valor:,.2f} via {trail.instrumento} ({trail.data_referencia})"
                )

    def _gerar_acoes_imediatas(self, report: DailyIntelligenceReport) -> None:
        if any(a.categoria == "SISBAJUD — Não Resposta" for a in report.alertas_criticos):
            report.acoes_imediatas.append(
                "URGENTE: Peticionar contra FRAM/OSLO por descumprimento de ordem judicial"
            )
        if any(a.categoria == "FIP — Side-Pocket" for a in report.alertas_criticos):
            report.acoes_imediatas.append(
                "URGENTE: Requerer perícia contábil no FRAM XIV FIP"
            )
        if any(a.categoria == "FIP — Estrutura Fraudulenta" for a in report.alertas_criticos):
            report.acoes_imediatas.append(
                "URGENTE: Arguir fraude à execução — Bonifácio FIP constituído pós-litígio"
            )
        if any(a.categoria == "Ativo — Variação Abrupta" for a in report.alertas_criticos):
            report.acoes_imediatas.append(
                "URGENTE: Rastrear destinatário do esvaziamento Itaú R$ 469.575 → R$ 5.491"
            )
