"""
Dados de investigação para o caso de referência.
Representa o estado atual do Whole Money Trail e dos ativos mapeados.
"""
from datetime import date
from decimal import Decimal

from models.assets import Asset, FIP, ClasseFIP, SisbajudCode, SisbajudResponse
from models.institutions import Institution, InstitutionStatus
from models.case import Case, CaseStatus, LegalFramework, WholeMoneyTrail


def criar_caso_investigacao() -> Case:
    # ── FIPs investigados ──────────────────────────────────────────────
    fram = FIP(
        nome="FRAM XIV FIP",
        cnpj="40.000.000/0001-91",
        administrador="Oslo Capital Gestora",
        pl_declarado=Decimal("3877255.47"),
        pl_cvm=Decimal("3877255.47"),
        data_constituicao=date(2019, 6, 10),
        classes=[
            ClasseFIP(
                nome="Classe A",
                data_criacao=date(2019, 6, 10),
                pl=Decimal("1200000.00"),
            ),
            ClasseFIP(
                nome="Classe J",
                data_criacao=date(2024, 3, 15),
                pl=Decimal("950000.00"),
                criada_pos_litigio=True,
                regulamento_alterado=True,
            ),
            ClasseFIP(
                nome="Side-Pocket",
                data_criacao=date(2024, 7, 22),
                pl=Decimal("1727255.47"),
                side_pocket=True,
                criada_pos_litigio=True,
            ),
        ],
    )

    bonifacio = FIP(
        nome="BONIFÁCIO FIP",
        cnpj="73.000.000/0001-62",
        administrador="Gestor Bonifácio",
        pl_declarado=Decimal("8500000.00"),
        pl_cvm=Decimal("8500000.00"),
        data_constituicao=date(2023, 11, 1),
        classes=[
            ClasseFIP(
                nome="Única",
                data_criacao=date(2023, 11, 1),
                pl=Decimal("8500000.00"),
                criada_pos_litigio=True,
            ),
        ],
    )

    ajaccio = FIP(
        nome="AJACCIO INVESTIMENTOS FIP",
        cnpj="61.000.000/0001-00",
        administrador="Ajaccio Gestão",
        pl_declarado=Decimal("2100000.00"),
        pl_cvm=Decimal("2100000.00"),
        data_constituicao=date(2020, 1, 15),
        ativo=False,
        classes=[
            ClasseFIP(
                nome="Classe I",
                data_criacao=date(2020, 1, 15),
                pl=Decimal("2100000.00"),
                regulamento_alterado=True,
            ),
        ],
    )

    # ── Ativos bancários ───────────────────────────────────────────────
    lig_itau = Asset(
        id="LIG-001",
        descricao="LIG Itaú — Letra Imobiliária Garantida",
        tipo="LIG",
        valor=Decimal("1250000.00"),
        instituicao="Itaú Unibanco S.A.",
        data_referencia=date(2024, 1, 1),
    )

    cdb_btg = Asset(
        id="CDB-001",
        descricao="CDB BTG Pactual",
        tipo="Renda Fixa",
        valor=Decimal("0.00"),
        instituicao="BTG Pactual S.A.",
        data_referencia=date(2024, 1, 10),
    )
    cdb_btg.registrar_variacao(Decimal("650758.60"))

    conta_itau = Asset(
        id="CC-001",
        descricao="Conta Corrente Itaú",
        tipo="Conta Corrente",
        valor=Decimal("5491.00"),
        instituicao="Itaú Unibanco S.A.",
        data_referencia=date(2024, 1, 10),
    )
    conta_itau.registrar_variacao(Decimal("469575.00"))

    # ── Instituições ───────────────────────────────────────────────────
    itau = Institution(
        nome="Itaú Unibanco S.A.",
        ispb="60701190",
        tipo="Banco Comercial",
        status=InstitutionStatus.DEGRADADO,
        sisbajud_response=SisbajudResponse(
            instituicao="Itaú Unibanco S.A.",
            codigo=SisbajudCode.RESPONDIDO_SEM_SALDO,
            valor_bloqueado=Decimal("5491.00"),
        ),
        saldo_atual=Decimal("5491.00"),
        saldo_anterior=Decimal("469575.00"),
    )
    itau.avaliar_esvaziamento()

    btg = Institution(
        nome="BTG Pactual S.A.",
        ispb="01526938",
        tipo="Banco de Investimento",
        status=InstitutionStatus.DEGRADADO,
        sisbajud_response=SisbajudResponse(
            instituicao="BTG Pactual S.A.",
            codigo=SisbajudCode.RESPONDIDO_SEM_SALDO,
            valor_bloqueado=Decimal("0"),
        ),
        saldo_atual=Decimal("0"),
        saldo_anterior=Decimal("650758.60"),
    )
    btg.avaliar_esvaziamento()

    oslo = Institution(
        nome="Oslo Capital / FRAM XIV FIP",
        ispb="00000000",
        tipo="Gestora FIP",
        status=InstitutionStatus.SEM_RESPOSTA,
        sisbajud_response=SisbajudResponse(
            instituicao="Oslo Capital",
            codigo=SisbajudCode.NAO_RESPONDEU,
        ),
        saldo_atual=None,
        saldo_anterior=None,
    )
    oslo.avaliar_nao_resposta()

    # ── Whole Money Trail ──────────────────────────────────────────────
    money_trail = [
        WholeMoneyTrail(
            data_referencia=date(2024, 1, 8),
            origem="Conta Corrente Itaú (réu)",
            destino="Conta desconhecida — TED",
            valor=Decimal("464084.00"),
            instrumento="TED",
            suspeito=True,
            justificativa_suspeita="Transferência 2 dias antes da ordem SISBAJUD",
        ),
        WholeMoneyTrail(
            data_referencia=date(2024, 1, 9),
            origem="CDB BTG Pactual (réu)",
            destino="Conta desconhecida — PIX",
            valor=Decimal("650758.60"),
            instrumento="PIX",
            suspeito=True,
            justificativa_suspeita="Liquidação do CDB 1 dia antes da ordem SISBAJUD",
        ),
        WholeMoneyTrail(
            data_referencia=date(2023, 11, 1),
            origem="Réu (cotista)",
            destino="Bonifácio FIP",
            valor=Decimal("8500000.00"),
            instrumento="Integralização de cotas",
            suspeito=True,
            justificativa_suspeita="FIP constituído após distribuição do processo",
        ),
        WholeMoneyTrail(
            data_referencia=date(2024, 7, 22),
            origem="FRAM XIV FIP — Ativos",
            destino="Side-Pocket FRAM",
            valor=Decimal("1727255.47"),
            instrumento="Segregação interna FIP",
            suspeito=True,
            justificativa_suspeita="Side-pocket criado durante litígio para dificultar bloqueio",
        ),
    ]

    # ── Caso ───────────────────────────────────────────────────────────
    case = Case(
        numero_processo="0012345-67.2023.8.26.0100",
        requerente="Credor S.A.",
        requerido="Devedor Ltda. / Sócio Controlador",
        valor_causa=Decimal("15000000.00"),
        data_distribuicao=date(2023, 9, 15),
        status=CaseStatus.BLOQUEIO_PARCIAL,
        frameworks_aplicaveis=[
            LegalFramework.FRAUDE_EXECUCAO_CPC792,
            LegalFramework.DESCONSIDERACAO_CC50,
            LegalFramework.FRAUDE_CP171,
            LegalFramework.LAVAGEM_9613,
        ],
        fips_investigados=[fram, bonifacio, ajaccio],
        ativos_mapeados=[lig_itau, cdb_btg, conta_itau],
        instituicoes=[itau, btg, oslo],
        money_trail=money_trail,
    )

    return case
