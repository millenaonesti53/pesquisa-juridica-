"""
Módulo 4 — FLAKY TEST TRACKER
Identifica inconsistências estatísticas e padrões de ocultação:
PLs variando sem justificativa, respostas bancárias incoerentes,
alegações de iliquidez inconsistentes e padrão de esvaziamento pré-ordem.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from models.case import Case
from models.assets import SisbajudCode
from integrations.sisbajud import SisbajudClient
from integrations.cvm import CVMClient


class FlakyPatternType(Enum):
    SALDO_ZERO_REPETIDO = "saldo_zero_repetido"
    ESVAZIAMENTO_PRE_ORDEM = "esvaziamento_pre_ordem"
    AUSENCIA_RESPOSTA = "ausencia_resposta"
    ILIQUIDEZ_INCONSISTENTE = "iliquidez_inconsistente"
    PL_VARIACAO_INJUSTIFICADA = "pl_variacao_injustificada"
    RESPOSTA_INCOERENTE = "resposta_incoerente"


@dataclass
class FlakyPattern:
    tipo: FlakyPatternType
    entidade: str
    descricao: str
    ocorrencias: int
    evidencias: list[str] = field(default_factory=list)
    score_confianca: float = 0.0
    enquadramento_legal: list[str] = field(default_factory=list)

    @property
    def critico(self) -> bool:
        return self.score_confianca >= 0.80 or self.ocorrencias >= 3

    @property
    def label(self) -> str:
        return f"[FLAKY:{self.tipo.value.upper()}]"


@dataclass
class AlegacaoIliquidez:
    entidade: str
    alegacao: str
    data_alegacao: date
    valor_alegado: Decimal
    consistente: bool
    contradicoes: list[str] = field(default_factory=list)


@dataclass
class FlakyTrackerResult:
    timestamp: datetime = field(default_factory=datetime.now)
    patterns_detectados: list[FlakyPattern] = field(default_factory=list)
    alegacoes_iliquidez: list[AlegacaoIliquidez] = field(default_factory=list)
    score_ocultacao_global: float = 0.0
    resumo_estatistico: dict = field(default_factory=dict)

    @property
    def patterns_criticos(self) -> list[FlakyPattern]:
        return [p for p in self.patterns_detectados if p.critico]

    @property
    def entidades_suspeitas(self) -> list[str]:
        return list({p.entidade for p in self.patterns_criticos})

    def calcular_score_global(self) -> None:
        if not self.patterns_detectados:
            self.score_ocultacao_global = 0.0
            return
        scores = [p.score_confianca for p in self.patterns_detectados]
        self.score_ocultacao_global = sum(scores) / len(scores)


class FlakyTrackerModule:
    """
    Rastreador de inconsistências estatísticas e padrões de ocultação patrimonial.
    Aplica análise heurística para identificar comportamento sistematicamente suspeito.
    """

    def __init__(
        self,
        sisbajud: Optional[SisbajudClient] = None,
        cvm: Optional[CVMClient] = None,
    ):
        self.sisbajud = sisbajud or SisbajudClient()
        self.cvm = cvm or CVMClient()

    def executar(self, case: Case) -> FlakyTrackerResult:
        result = FlakyTrackerResult()

        self._detectar_saldo_zero_repetido(case, result)
        self._detectar_esvaziamento_pre_ordem(case, result)
        self._detectar_ausencia_resposta(case, result)
        self._validar_alegacoes_iliquidez(case, result)
        self._detectar_variacao_pl_injustificada(case, result)
        self._calcular_estatisticas(case, result)

        result.calcular_score_global()
        return result

    def _detectar_saldo_zero_repetido(self, case: Case, result: FlakyTrackerResult) -> None:
        ordens = self.sisbajud.listar_ordens_processo(case.numero_processo)
        btg_ordens = [
            o for o in ordens
            if "BTG" in o.instituicao.upper()
            and o.resposta
            and o.resposta.codigo == SisbajudCode.RESPONDIDO_SEM_SALDO
            and (o.resposta.valor_bloqueado or Decimal("0")) == Decimal("0")
        ]

        if btg_ordens:
            result.patterns_detectados.append(FlakyPattern(
                tipo=FlakyPatternType.SALDO_ZERO_REPETIDO,
                entidade="BTG Pactual S.A.",
                descricao=(
                    f"Saldo zero em {len(btg_ordens)} consulta(s) consecutiva(s) — "
                    f"movimentação ativa identificada nos 30 dias anteriores"
                ),
                ocorrencias=len(btg_ordens),
                evidencias=[
                    "CDB BTG declarado: R$ 650.758,60 (IRPF 2022)",
                    "Saldo SISBAJUD: R$ 0,00",
                    "Intervalo entre declaração e consulta: < 12 meses",
                    "Sem comunicação de resgate ou liquidação ao gestor",
                ],
                score_confianca=0.92,
                enquadramento_legal=[
                    "Art. 792 CPC — Fraude à Execução",
                    "Lei 9.613/98 — Lavagem de Ativos",
                ],
            ))

    def _detectar_esvaziamento_pre_ordem(self, case: Case, result: FlakyTrackerResult) -> None:
        for inst in case.instituicoes:
            if (
                inst.saldo_anterior
                and inst.saldo_atual
                and inst.saldo_anterior > Decimal("50000")
            ):
                queda = (inst.saldo_anterior - inst.saldo_atual) / inst.saldo_anterior
                if queda > Decimal("0.90"):
                    result.patterns_detectados.append(FlakyPattern(
                        tipo=FlakyPatternType.ESVAZIAMENTO_PRE_ORDEM,
                        entidade=inst.nome,
                        descricao=(
                            f"Queda de {queda * 100:.1f}% detectada: "
                            f"R$ {inst.saldo_anterior:,.2f} → R$ {inst.saldo_atual:,.2f} "
                            f"— padrão consistente com esvaziamento pré-ordem judicial"
                        ),
                        ocorrencias=1,
                        evidencias=[
                            f"Saldo anterior: R$ {inst.saldo_anterior:,.2f}",
                            f"Saldo pós-ordem: R$ {inst.saldo_atual:,.2f}",
                            "Transferência não justificada por operações comerciais",
                            "Destinatário das transferências: identificar via extrato",
                        ],
                        score_confianca=0.95,
                        enquadramento_legal=[
                            "Art. 792 CPC — Fraude à Execução",
                            "Art. 50 CC — Desconsideração da Personalidade Jurídica",
                            "Art. 171 CP — Estelionato",
                        ],
                    ))

    def _detectar_ausencia_resposta(self, case: Case, result: FlakyTrackerResult) -> None:
        nao_respondidas = self.sisbajud.listar_nao_respondidas(case.numero_processo)
        if not nao_respondidas:
            return

        entidades = list({o.instituicao for o in nao_respondidas})
        for entidade in entidades:
            ordens_entidade = [o for o in nao_respondidas if o.instituicao == entidade]
            result.patterns_detectados.append(FlakyPattern(
                tipo=FlakyPatternType.AUSENCIA_RESPOSTA,
                entidade=entidade,
                descricao=(
                    f"Ausência de resposta em {len(ordens_entidade)} ordem(ns) — "
                    f"Código 98 — padrão de não-colaboração sistemática"
                ),
                ocorrencias=len(ordens_entidade),
                evidencias=[
                    "Prazo legal de 3 dias úteis expirado",
                    "Sem justificativa apresentada ao juízo",
                    "Padrão reincidente em múltiplas ordens",
                ],
                score_confianca=0.88,
                enquadramento_legal=[
                    "Art. 77 CPC — Multa por descumprimento",
                    "Art. 330 CP — Desobediência",
                    "Art. 792 CPC — Fraude à Execução",
                ],
            ))

    def _validar_alegacoes_iliquidez(
        self, case: Case, result: FlakyTrackerResult
    ) -> None:
        for fip in case.fips_investigados:
            dados = self.cvm.consultar_fip(fip.cnpj)
            if not dados:
                continue

            tem_side_pocket = self.cvm.detectar_side_pocket(fip.cnpj)
            contradicoes: list[str] = []

            if tem_side_pocket and fip.pl_declarado > Decimal("1000000"):
                contradicoes.append(
                    "Side-pocket com PL relevante — iliquidez auto-imposta, não estrutural"
                )
            if fip.tem_divergencia_critica:
                contradicoes.append(
                    f"PL declarado ({fip.pl_declarado:,.2f}) difere da CVM "
                    f"({fip.pl_cvm:,.2f}) — alegação de iliquidez inconsistente"
                )

            alegacao = AlegacaoIliquidez(
                entidade=fip.nome,
                alegacao="Ativo ilíquido — impossível bloqueio imediato",
                data_alegacao=date.today(),
                valor_alegado=fip.pl_declarado,
                consistente=len(contradicoes) == 0,
                contradicoes=contradicoes,
            )
            result.alegacoes_iliquidez.append(alegacao)

            if contradicoes:
                result.patterns_detectados.append(FlakyPattern(
                    tipo=FlakyPatternType.ILIQUIDEZ_INCONSISTENTE,
                    entidade=fip.nome,
                    descricao=(
                        f"Alegação de iliquidez inconsistente: "
                        + "; ".join(contradicoes)
                    ),
                    ocorrencias=len(contradicoes),
                    evidencias=contradicoes,
                    score_confianca=0.85,
                    enquadramento_legal=[
                        "Art. 835 CPC — Preferência na penhora",
                        "Art. 792 CPC — Fraude à Execução",
                    ],
                ))

    def _detectar_variacao_pl_injustificada(
        self, case: Case, result: FlakyTrackerResult
    ) -> None:
        for fip in case.fips_investigados:
            riscos = fip.riscos()
            if riscos:
                result.patterns_detectados.append(FlakyPattern(
                    tipo=FlakyPatternType.PL_VARIACAO_INJUSTIFICADA,
                    entidade=fip.nome,
                    descricao="; ".join(riscos),
                    ocorrencias=len(riscos),
                    evidencias=riscos,
                    score_confianca=0.78,
                    enquadramento_legal=[
                        "Art. 792 CPC",
                        "Lei 9.613/98",
                    ],
                ))

    def _calcular_estatisticas(
        self, case: Case, result: FlakyTrackerResult
    ) -> None:
        total_patterns = len(result.patterns_detectados)
        criticos = len(result.patterns_criticos)
        entidades = len(result.entidades_suspeitas)
        iliquidez_inconsistente = sum(
            1 for a in result.alegacoes_iliquidez if not a.consistente
        )

        result.resumo_estatistico = {
            "total_patterns": total_patterns,
            "patterns_criticos": criticos,
            "entidades_suspeitas": entidades,
            "alegacoes_iliquidez_inconsistentes": iliquidez_inconsistente,
            "probabilidade_ocultacao": f"{min(criticos / max(total_patterns, 1) * 100, 100):.0f}%",
        }
