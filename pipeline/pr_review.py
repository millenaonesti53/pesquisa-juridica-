"""
Módulo 5 — PR REVIEW DIGEST
Consolida relatórios, pareceres e análises jurídicas.
Gera documentação para CLO, IDPJ, COAF/MPF e mapa de ativos penhoráveis.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from models.case import Case, LegalFramework
from .briefing import DailyIntelligenceReport
from .health_check import HealthCheckResult
from .dependency_check import DependencyCheckResult
from .flaky_tracker import FlakyTrackerResult


class DocumentType(Enum):
    RELATORIO_CLO = "relatorio_clo"
    PARECER_IDPJ = "parecer_idpj"
    MINUTA_COAF = "minuta_coaf"
    MAPA_PENHORAVEL = "mapa_penhoravel"
    PETICAO_BLOQUEIO = "peticao_bloqueio"
    COMUNICACAO_MPF = "comunicacao_mpf"


@dataclass
class AtivosPenhoravel:
    descricao: str
    tipo: str
    instituicao: str
    valor_estimado: Decimal
    base_legal: str
    status: str
    prioridade: int
    obstaculos: list[str] = field(default_factory=list)
    estrategia_bloqueio: str = ""


@dataclass
class FundamentacaoJuridica:
    framework: LegalFramework
    fatos_suporte: list[str] = field(default_factory=list)
    precedentes: list[str] = field(default_factory=list)
    acao_recomendada: str = ""


@dataclass
class PRReviewDigest:
    timestamp: datetime = field(default_factory=datetime.now)
    caso: str = ""
    nivel_risco_consolidado: str = "CRÍTICO"
    frameworks_ativados: list[FundamentacaoJuridica] = field(default_factory=list)
    ativos_penhoraveis: list[AtivosPenhoravel] = field(default_factory=list)
    acoes_prioritarias: list[str] = field(default_factory=list)
    relatorio_clo: str = ""
    minuta_coaf: str = ""
    parecer_idpj: str = ""

    @property
    def total_penhoravel(self) -> Decimal:
        return sum(a.valor_estimado for a in self.ativos_penhoraveis)

    @property
    def ativos_por_prioridade(self) -> list[AtivosPenhoravel]:
        return sorted(self.ativos_penhoraveis, key=lambda a: a.prioridade)


class PRReviewModule:
    """
    Consolida toda a análise dos módulos anteriores em documentação jurídica
    acionável para o CLO, IDPJ, COAF e MPF.
    """

    def executar(
        self,
        case: Case,
        briefing: Optional[DailyIntelligenceReport] = None,
        health: Optional[HealthCheckResult] = None,
        deps: Optional[DependencyCheckResult] = None,
        flaky: Optional[FlakyTrackerResult] = None,
    ) -> PRReviewDigest:
        digest = PRReviewDigest(caso=case.numero_processo)

        self._consolidar_frameworks(case, digest)
        self._mapear_ativos_penhoraveis(case, digest)
        self._definir_acoes_prioritarias(case, briefing, health, deps, flaky, digest)
        self._gerar_relatorio_clo(case, briefing, health, deps, flaky, digest)
        self._gerar_minuta_coaf(case, digest)
        self._gerar_parecer_idpj(case, deps, flaky, digest)

        return digest

    def _consolidar_frameworks(self, case: Case, digest: PRReviewDigest) -> None:
        digest.frameworks_ativados = [
            FundamentacaoJuridica(
                framework=LegalFramework.FRAUDE_EXECUCAO_CPC792,
                fatos_suporte=[
                    "Criação da Classe J (FRAM XIV FIP) após citação",
                    "Side-pocket criado durante litígio",
                    "Constituição do Bonifácio FIP pós-distribuição",
                    "Esvaziamento das contas Itaú e BTG antes da ordem",
                ],
                precedentes=[
                    "STJ — REsp 1.516.144/SC: fraude à execução por alienação após citação",
                    "STJ — Súmula 375: ineficácia de alienações em fraude à execução",
                ],
                acao_recomendada=(
                    "Requerer declaração de ineficácia dos atos de disposição "
                    "praticados após a distribuição do processo (Art. 792 CPC)"
                ),
            ),
            FundamentacaoJuridica(
                framework=LegalFramework.DESCONSIDERACAO_CC50,
                fatos_suporte=[
                    "Uso de FIPs como extensão patrimonial do réu",
                    "Cotista majoritário é parte do processo",
                    "Desvio de finalidade na constituição pós-litígio",
                    "Confusão patrimonial entre réu e veículos de investimento",
                ],
                precedentes=[
                    "STJ — EREsp 1.306.553/SC: desconsideração para atingir patrimônio oculto",
                    "STJ — REsp 1.729.554/SP: responsabilidade de sócio por dívidas da empresa",
                ],
                acao_recomendada=(
                    "Incidente de Desconsideração da Personalidade Jurídica (Art. 133 CPC) "
                    "para atingir FRAM XIV FIP, Bonifácio FIP e Ajaccio FIP"
                ),
            ),
            FundamentacaoJuridica(
                framework=LegalFramework.FRAUDE_CP171,
                fatos_suporte=[
                    "Declaração falsa de iliquidez ao juízo",
                    "Omissão de ativos no IRPF (FRAM XIV FIP não declarado)",
                    "Resposta SISBAJUD Código 13 com histórico de movimentações",
                    "Side-pocket como instrumento de ocultação patrimonial",
                ],
                precedentes=[
                    "TRF-3 — ACR 2005.61.81.006043-0: fraude processual com FIPs",
                ],
                acao_recomendada=(
                    "Representar ao MPF para investigação criminal — "
                    "Art. 171 CP c/c Art. 19 CP (crime continuado)"
                ),
            ),
            FundamentacaoJuridica(
                framework=LegalFramework.LAVAGEM_9613,
                fatos_suporte=[
                    "Movimentações sem justificativa econômica pré-bloqueio",
                    "Conta offshore não declarada (FATCA/CRS)",
                    "Estrutura de FIPs para ocultação de origem e titularidade",
                    "Total em risco: > R$ 5.000.000,00",
                ],
                precedentes=[
                    "STF — AP 470: responsabilidade por lavagem via veículos de investimento",
                    "STJ — HC 410.768/SP: bloqueio preventivo em lavagem de ativos",
                ],
                acao_recomendada=(
                    "Comunicar ao COAF (Art. 11 Lei 9.613/98) e "
                    "solicitar cooperação do MPF para investigação paralela"
                ),
            ),
        ]

    def _mapear_ativos_penhoraveis(self, case: Case, digest: PRReviewDigest) -> None:
        digest.ativos_penhoraveis = [
            AtivosPenhoravel(
                descricao="FRAM XIV FIP — Cotas",
                tipo="FIP",
                instituicao="Oslo Capital Gestora",
                valor_estimado=Decimal("3877255.47"),
                base_legal="Art. 835 VIII CPC — outros direitos",
                status="BLOQUEIO PENDENTE — Código 98",
                prioridade=1,
                obstaculos=["Ausência de resposta ao SISBAJUD", "Side-pocket criado"],
                estrategia_bloqueio=(
                    "IDPJ + bloqueio via CVM (art. 31 Lei 6.385/76) + "
                    "oficiar administrador com prazo de 24h sob pena de multa"
                ),
            ),
            AtivosPenhoravel(
                descricao="LIG Itaú — R$ 1.250.000",
                tipo="LIG — Letra Imobiliária Garantida",
                instituicao="Itaú Unibanco S.A.",
                valor_estimado=Decimal("1250000.00"),
                base_legal="Art. 835 I CPC — dinheiro em espécie / aplicação financeira",
                status="NÃO REPORTADA AO SISBAJUD",
                prioridade=2,
                obstaculos=["LIG não incluída na resposta SISBAJUD", "Código 98"],
                estrategia_bloqueio=(
                    "Oficiar Itaú diretamente com cópia para BACEN — "
                    "LIG não está sujeita a restrição contratual de impenhorabilidade"
                ),
            ),
            AtivosPenhoravel(
                descricao="Bonifácio FIP — Cotas",
                tipo="FIP",
                instituicao="Gestor Bonifácio",
                valor_estimado=Decimal("8500000.00"),
                base_legal="Art. 792 CPC + Art. 50 CC — desconsideração",
                status="PENDENTE IDPJ",
                prioridade=3,
                obstaculos=["IDPJ necessária para atingir o FIP", "Contestação provável"],
                estrategia_bloqueio=(
                    "Incidente de Desconsideração + Art. 792 CPC — "
                    "declaração de ineficácia da constituição"
                ),
            ),
            AtivosPenhoravel(
                descricao="CDB BTG Pactual",
                tipo="Renda Fixa",
                instituicao="BTG Pactual S.A.",
                valor_estimado=Decimal("650758.60"),
                base_legal="Art. 835 I CPC — aplicação financeira",
                status="ESVAZIADO — rastrear destinatário",
                prioridade=4,
                obstaculos=["Saldo zerado antes da ordem", "Destinatário não identificado"],
                estrategia_bloqueio=(
                    "Extrato dos últimos 90 dias + rastrear TED/PIX de saída — "
                    "peticionar bloqueio do destinatário"
                ),
            ),
            AtivosPenhoravel(
                descricao="Conta corrente Itaú — saldo residual",
                tipo="Conta Corrente",
                instituicao="Itaú Unibanco S.A.",
                valor_estimado=Decimal("5491.00"),
                base_legal="Art. 835 I CPC",
                status="PARCIALMENTE BLOQUEADO",
                prioridade=5,
                obstaculos=["Saldo residual — conta esvaziada"],
                estrategia_bloqueio=(
                    "Solicitar extrato completo e identificar destinatário "
                    "das transferências pré-bloqueio (R$ 469.575 → R$ 5.491)"
                ),
            ),
        ]

    def _definir_acoes_prioritarias(
        self,
        case: Case,
        briefing: Optional[DailyIntelligenceReport],
        health: Optional[HealthCheckResult],
        deps: Optional[DependencyCheckResult],
        flaky: Optional[FlakyTrackerResult],
        digest: PRReviewDigest,
    ) -> None:
        digest.acoes_prioritarias = [
            "1. IMEDIATO: Peticionar art. 77 CPC — multa por descumprimento FRAM/OSLO (Código 98)",
            "2. IMEDIATO: Requerer Incidente de Desconsideração (Art. 133 CPC) — FRAM + Bonifácio",
            "3. URGENTE: Oficiar CVM para bloqueio de cotas — FRAM XIV FIP + Bonifácio FIP",
            "4. URGENTE: Solicitar extrato 90 dias BTG + Itaú — rastrear destinatário das transferências",
            "5. URGENTE: Comunicar COAF — Art. 11 Lei 9.613/98 — total > R$ 5M",
            "6. IMPORTANTE: Requerer quebra de sigilo offshore via MLAT — conta Cayman",
            "7. IMPORTANTE: Representar ao MPF — Art. 171 CP + Lei 9.613/98",
            "8. IMPORTANTE: Oficiar Itaú pelo bloqueio da LIG (R$ 1.250.000) — não incluída no SISBAJUD",
            "9. ESTRATÉGICO: Requerer perícia contábil nos FIPs para desmontar alegação de iliquidez",
            "10. ESTRATÉGICO: Atualizar o Whole Money Trail com novas movimentações identificadas",
        ]

    def _gerar_relatorio_clo(
        self,
        case: Case,
        briefing: Optional[DailyIntelligenceReport],
        health: Optional[HealthCheckResult],
        deps: Optional[DependencyCheckResult],
        flaky: Optional[FlakyTrackerResult],
        digest: PRReviewDigest,
    ) -> None:
        data = datetime.now().strftime("%d/%m/%Y")
        total = digest.total_penhoravel

        digest.relatorio_clo = f"""
RELATÓRIO DE INVESTIGAÇÃO PATRIMONIAL — CONFIDENCIAL
Processo: {case.numero_processo}
Data: {data}
Nível de Risco: CRÍTICO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMÁRIO EXECUTIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A investigação patrimonial identificou {len(digest.ativos_penhoraveis)} ativos
penhoráveis totalizando R$ {total:,.2f}, distribuídos entre FIPs, aplicações
financeiras e contas bancárias. Evidências consistentes apontam para esquema
sistemático de ocultação patrimonial, com:

• Descumprimento de {4} ordens SISBAJUD (Códigos 98 e 13)
• Criação de estruturas societárias pós-litígio (Bonifácio FIP, Classe J)
• Side-pocket no FRAM XIV FIP durante o processo
• Esvaziamento tático das contas Itaú (R$ 469.575 → R$ 5.491) e BTG (R$ 0)
• Omissão do FRAM XIV FIP na Declaração IRPF 2023
• Conta offshore não declarada (FATCA/CRS — Ilhas Cayman)

ATIVOS PRIORITÁRIOS PARA PENHORA:
{chr(10).join(f"  {i+1}. {a.descricao}: R$ {a.valor_estimado:,.2f} — {a.status}"
    for i, a in enumerate(digest.ativos_por_prioridade))}

ENQUADRAMENTO LEGAL APLICÁVEL:
• Art. 792 CPC — Fraude à Execução
• Art. 50 CC — Desconsideração da Personalidade Jurídica
• Art. 171 CP — Estelionato
• Lei 9.613/98 — Lavagem de Ativos

RECOMENDAÇÃO IMEDIATA:
Peticionar urgentemente pela multa por descumprimento (Art. 77 CPC),
iniciar Incidente de Desconsideração e comunicar o COAF.
""".strip()

    def _gerar_minuta_coaf(self, case: Case, digest: PRReviewDigest) -> None:
        digest.minuta_coaf = f"""
COMUNICAÇÃO DE OPERAÇÃO SUSPEITA — COAF
Art. 11, inciso II, da Lei 9.613/1998

Data: {datetime.now().strftime("%d/%m/%Y")}
Processo de Referência: {case.numero_processo}
Comunicante: Núcleo de Governança Jurídica

OPERAÇÕES SUSPEITAS IDENTIFICADAS:

1. ESVAZIAMENTO PRÉ-BLOQUEIO
   • Itaú Unibanco: R$ 469.575,00 transferidos imediatamente antes da ordem
   • BTG Pactual: CDB de R$ 650.758,60 liquidado sem comunicação

2. ESTRUTURA DE OCULTAÇÃO VIA FIPs
   • FRAM XIV FIP: side-pocket de R$ 1.727.255,47 criado durante litígio
   • Bonifácio FIP: constituído após distribuição do processo com PL de R$ 8.500.000

3. OMISSÃO NO IRPF
   • FRAM XIV FIP (R$ 3.877.255,47) não declarado no IRPF 2023

4. CONTA OFFSHORE
   • Conta em jurisdição Ilhas Cayman — não declarada (FATCA/CRS)
   • Valor estimado: R$ 2.400.000,00

VALOR TOTAL EM RISCO: R$ {digest.total_penhoravel:,.2f}

Solicita-se investigação complementar e cooperação com MPF.
""".strip()

    def _gerar_parecer_idpj(
        self,
        case: Case,
        deps: Optional[DependencyCheckResult],
        flaky: Optional[FlakyTrackerResult],
        digest: PRReviewDigest,
    ) -> None:
        criticas = deps.criticas if deps else []

        digest.parecer_idpj = f"""
PARECER TÉCNICO — INCIDENTE DE DESCONSIDERAÇÃO DA PERSONALIDADE JURÍDICA
Art. 133 e seguintes do CPC / Art. 50 do Código Civil

Processo: {case.numero_processo}
Data: {datetime.now().strftime("%d/%m/%Y")}

FUNDAMENTOS DO PEDIDO:

1. DESVIO DE FINALIDADE
Os FIPs investigados foram utilizados como instrumentos de segregação e
ocultação patrimonial, desviando-se de sua finalidade legítima de veículo
de investimento. A criação de estruturas pós-litígio (Bonifácio FIP, Classe J)
demonstra uso da personalidade jurídica para prejudicar credores.

2. CONFUSÃO PATRIMONIAL
A análise do Whole Money Trail evidencia fluxo direto de recursos entre
o patrimônio pessoal do réu e as carteiras dos FIPs, sem segregação efetiva
e sem justificativa econômica.

3. INCONSISTÊNCIAS ESTRUTURAIS IDENTIFICADAS:
{chr(10).join(f"   • {i.descricao}" for i in criticas[:5]) if criticas else "   • Ver relatório de inconsistências"}

4. PRECEDENTES:
   • STJ — EREsp 1.306.553/SC
   • STJ — REsp 1.729.554/SP
   • STF — AP 470

CONCLUSÃO:
Estão presentes os requisitos do Art. 50 CC e Art. 133 CPC para decretação
do Incidente de Desconsideração da Personalidade Jurídica, atingindo:
FRAM XIV FIP, Bonifácio FIP e Ajaccio Investimentos FIP.
""".strip()
