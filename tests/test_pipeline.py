"""
Testes de integração do Pipeline Cognitivo Corporativo.
Verifica a detecção correta de padrões de ocultação, inconsistências e alertas.
"""
import pytest
from decimal import Decimal
from datetime import date

from fixtures import criar_caso_investigacao
from models.assets import SisbajudCode, ClasseFIP, FIP
from models.institutions import Institution, RiskLevel
from pipeline.briefing import BriefingModule
from pipeline.health_check import HealthCheckModule, ComponentStatus
from pipeline.dependency_check import DependencyCheckModule
from pipeline.flaky_tracker import FlakyTrackerModule, FlakyPatternType
from pipeline.pr_review import PRReviewModule


@pytest.fixture
def case():
    return criar_caso_investigacao()


# ── Módulo 1: Briefing ─────────────────────────────────────────────────────


class TestBriefing:
    def test_detecta_nao_resposta_sisbajud(self, case):
        report = BriefingModule().executar(case)
        criticos = [a for a in report.alertas_criticos if "Não Resposta" in a.categoria]
        assert len(criticos) >= 1

    def test_detecta_side_pocket_fram(self, case):
        report = BriefingModule().executar(case)
        sp = [a for a in report.alertas_criticos if "Side-Pocket" in a.categoria]
        assert len(sp) >= 1

    def test_detecta_classe_pos_litigio(self, case):
        report = BriefingModule().executar(case)
        fraude = [a for a in report.alertas_criticos if "Estrutura Fraudulenta" in a.categoria]
        assert len(fraude) >= 1

    def test_nivel_risco_critico(self, case):
        report = BriefingModule().executar(case)
        assert report.nivel_risco_geral == "CRÍTICO"

    def test_gera_acoes_imediatas(self, case):
        report = BriefingModule().executar(case)
        assert len(report.acoes_imediatas) >= 3

    def test_status_institucional_preenchido(self, case):
        report = BriefingModule().executar(case)
        assert len(report.status_institucional) > 0

    def test_whole_money_trail_registrado(self, case):
        report = BriefingModule().executar(case)
        suspeitos = [t for t in report.whole_money_trail_resumo if "[SUSPEITO]" in t]
        assert len(suspeitos) == len(case.money_trail)


# ── Módulo 2: Health Check ─────────────────────────────────────────────────


class TestHealthCheck:
    def test_sistema_instavel(self, case):
        result = HealthCheckModule().executar(case)
        assert not result.sistema_estavel

    def test_fram_oslo_indisponivel(self, case):
        result = HealthCheckModule().executar(case)
        indisponiveis = [
            c for c in result.componentes
            if c.status == ComponentStatus.INDISPONIVEL
        ]
        assert len(indisponiveis) >= 1
        assert any("FRAM" in c.nome or "OSLO" in c.nome for c in indisponiveis)

    def test_detecta_esvaziamento_itau(self, case):
        result = HealthCheckModule().executar(case)
        esvaziamentos = [
            r for r in result.riscos_patrimoniais if r.tipo_risco == "OCULTAÇÃO_CRÍTICA"
        ]
        assert len(esvaziamentos) >= 1

    def test_detecta_descumprimento_sisbajud(self, case):
        result = HealthCheckModule().executar(case)
        descumprimentos = [
            r for r in result.riscos_patrimoniais if r.tipo_risco == "DESCUMPRIMENTO_JUDICIAL"
        ]
        assert len(descumprimentos) >= 1

    def test_alerta_coaf_gerado(self, case):
        result = HealthCheckModule().executar(case)
        coaf = [a for a in result.alertas_ocultacao if "COAF" in a]
        assert len(coaf) >= 1

    def test_risco_total_critico(self, case):
        result = HealthCheckModule().executar(case)
        assert result.nivel_risco_total == "CRÍTICO"


# ── Módulo 3: Dependency Check ─────────────────────────────────────────────


class TestDependencyCheck:
    def test_detecta_classe_j_pos_litigio(self, case):
        result = DependencyCheckModule().executar(case)
        classes = [i for i in result.inconsistencias if i.tipo == "CLASSE_NOVA"]
        assert len(classes) >= 1
        assert all(i.pos_litigio for i in classes)

    def test_detecta_side_pocket(self, case):
        result = DependencyCheckModule().executar(case)
        sps = [i for i in result.inconsistencias if i.tipo == "SIDE_POCKET"]
        assert len(sps) >= 1

    def test_detecta_spv_bonifacio(self, case):
        result = DependencyCheckModule().executar(case)
        spvs = [i for i in result.inconsistencias if i.tipo == "SPV_NOVO"]
        assert len(spvs) >= 1
        assert any("BONIFÁCIO" in i.entidade.upper() for i in spvs)

    def test_criticas_sao_pos_litigio(self, case):
        result = DependencyCheckModule().executar(case)
        assert all(c.pos_litigio for c in result.criticas)

    def test_detecta_omissao_irpf_fram(self, case):
        result = DependencyCheckModule().executar(case)
        assert len(result.omissoes_irpf) >= 1
        assert any("FRAM" in o.get("ativo", "").upper() for o in result.omissoes_irpf)

    def test_divergencia_fatca(self, case):
        result = DependencyCheckModule().executar(case)
        assert len(result.divergencias_fatca) >= 1


# ── Módulo 4: Flaky Tracker ────────────────────────────────────────────────


class TestFlakyTracker:
    def test_detecta_saldo_zero_btg(self, case):
        result = FlakyTrackerModule().executar(case)
        zeros = [
            p for p in result.patterns_detectados
            if p.tipo == FlakyPatternType.SALDO_ZERO_REPETIDO
        ]
        assert len(zeros) >= 1
        assert any("BTG" in p.entidade for p in zeros)

    def test_detecta_esvaziamento_itau(self, case):
        result = FlakyTrackerModule().executar(case)
        esvaz = [
            p for p in result.patterns_detectados
            if p.tipo == FlakyPatternType.ESVAZIAMENTO_PRE_ORDEM
        ]
        assert len(esvaz) >= 1
        assert any("Itaú" in p.entidade for p in esvaz)

    def test_detecta_ausencia_resposta_oslo(self, case):
        result = FlakyTrackerModule().executar(case)
        ausencias = [
            p for p in result.patterns_detectados
            if p.tipo == FlakyPatternType.AUSENCIA_RESPOSTA
        ]
        assert len(ausencias) >= 1

    def test_score_ocultacao_alto(self, case):
        result = FlakyTrackerModule().executar(case)
        assert result.score_ocultacao_global >= 0.75

    def test_patterns_criticos_presentes(self, case):
        result = FlakyTrackerModule().executar(case)
        assert len(result.patterns_criticos) >= 3

    def test_estatisticas_calculadas(self, case):
        result = FlakyTrackerModule().executar(case)
        assert "total_patterns" in result.resumo_estatistico
        assert result.resumo_estatistico["total_patterns"] > 0


# ── Módulo 5: PR Review Digest ─────────────────────────────────────────────


class TestPRReview:
    def test_frameworks_ativados(self, case):
        digest = PRReviewModule().executar(case)
        assert len(digest.frameworks_ativados) == 4

    def test_ativos_penhoraveis_mapeados(self, case):
        digest = PRReviewModule().executar(case)
        assert len(digest.ativos_penhoraveis) >= 4

    def test_total_penhoravel_expressivo(self, case):
        digest = PRReviewModule().executar(case)
        assert digest.total_penhoravel > Decimal("5000000")

    def test_acoes_prioritarias_definidas(self, case):
        digest = PRReviewModule().executar(case)
        assert len(digest.acoes_prioritarias) >= 8

    def test_relatorio_clo_gerado(self, case):
        digest = PRReviewModule().executar(case)
        assert len(digest.relatorio_clo) > 100
        assert case.numero_processo in digest.relatorio_clo

    def test_minuta_coaf_gerada(self, case):
        digest = PRReviewModule().executar(case)
        assert "COAF" in digest.minuta_coaf
        assert "9.613" in digest.minuta_coaf

    def test_parecer_idpj_gerado(self, case):
        digest = PRReviewModule().executar(case)
        assert "Art. 133" in digest.parecer_idpj or "IDPJ" in digest.parecer_idpj
        assert "Art. 50" in digest.parecer_idpj


# ── Modelos ────────────────────────────────────────────────────────────────


class TestModelos:
    def test_sisbajud_code_98_risco(self):
        assert SisbajudCode.NAO_RESPONDEU.risco_ocultacao is True

    def test_sisbajud_code_13_risco(self):
        assert SisbajudCode.RESPONDIDO_SEM_SALDO.risco_ocultacao is True

    def test_sisbajud_code_01_sem_risco(self):
        assert SisbajudCode.BLOQUEIO_EFETUADO.risco_ocultacao is False

    def test_classe_fip_pos_litigio_risco(self):
        cls = ClasseFIP(
            nome="Classe J",
            data_criacao=date(2024, 3, 15),
            pl=Decimal("950000"),
            criada_pos_litigio=True,
        )
        riscos = cls.risco_estrutural()
        assert len(riscos) >= 1

    def test_institution_esvaziamento_risco_critico(self):
        from models.assets import SisbajudResponse
        from models.institutions import InstitutionStatus
        inst = Institution(
            nome="Teste",
            ispb="00000000",
            tipo="Banco",
            saldo_anterior=Decimal("469575"),
            saldo_atual=Decimal("5491"),
        )
        assert inst.risco == RiskLevel.CRITICO

    def test_case_cobertura_execucao(self, case):
        cobertura = case.cobertura_execucao
        assert cobertura > 0

    def test_case_ativos_variacao_suspeita(self, case):
        suspeitos = case.ativos_com_variacao_suspeita
        assert len(suspeitos) >= 1
