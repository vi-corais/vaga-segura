from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.modelos.evidencia import (
    EvidenciaColetada,
    Explicacao,
    ItemExplicacao,
    ResultadoAnalise,
    ResultadoColetor,
    Verificacao,
)
from app.modelos.extracao import Contatos, Contrato, ExtracaoOferta, Pagamento, Salario, VERSAO_ESQUEMA


def test_extracao_minima():
    e = ExtracaoOferta(e_oferta_de_trabalho=True)
    assert e.versao_esquema == VERSAO_ESQUEMA


def test_valor_informado_exige_trecho():
    with pytest.raises(ValidationError):
        Pagamento(forma="especie")
    with pytest.raises(ValidationError):
        Contrato(tipo="clt")
    with pytest.raises(ValidationError):
        Contatos(canal_exclusivo="whatsapp")
    assert Pagamento(forma="especie", trecho="pagamento em dinheiro").forma == "especie"


def test_nao_informado_dispensa_trecho():
    Pagamento()
    Contrato()
    Contatos()


def test_salario_min_maior_que_max():
    with pytest.raises(ValidationError):
        Salario(valor_min=3000, valor_max=2000, trecho="R$ 2 a 3 mil")


def test_coletor_nao_informa_pontos():
    """O coletor cria a evidência sem saber os pontos."""
    ev = EvidenciaColetada(id="cnpj_recente", coletor="cnpj", fonte="Receita Federal")
    with pytest.raises(ValidationError):
        EvidenciaColetada(id="cnpj_recente", coletor="cnpj", fonte="Receita Federal", pontos=-15)
    ResultadoColetor(
        verificacoes=[Verificacao(coletor="cnpj", verificacao="cnpj_idade", status="concluida")], evidencias=[ev]
    )


def test_verificacao_repetida():
    v = Verificacao(coletor="cnpj", verificacao="cnpj_situacao", status="concluida")
    with pytest.raises(ValidationError):
        ResultadoColetor(verificacoes=[v, v])


def test_guardrail_explicacao():
    base = dict(
        analise_id=uuid4(),
        criado_em=datetime.now(timezone.utc),
        versao_catalogo="0.3.0",
        versao_esquema=VERSAO_ESQUEMA,
        modelo_ia="qwen3:8b",
        origem="texto",
        canal="web",
        relacao_localidade="desconhecida",
        pontuacao=60,
        faixa="atencao",
        cobertura=0.5,
        evidencias=[],
        verificacoes=[],
    )
    ResultadoAnalise(**base, explicacao=Explicacao(resumo="ok", itens=[]))
    with pytest.raises(ValidationError):
        ResultadoAnalise(
            **base, explicacao=Explicacao(resumo="x", itens=[ItemExplicacao(evidencia_id="lista_suja_documento", texto="x")])
        )
