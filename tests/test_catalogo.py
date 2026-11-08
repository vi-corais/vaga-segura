import copy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from app.modelos.base import COLETORES
from app.modelos.catalogo import Catalogo, caminho_extracao_valido

CAMINHO = Path(__file__).resolve().parent.parent / "catalogo" / "evidencias.yaml"


@pytest.fixture
def dados():
    with CAMINHO.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_catalogo_valido(dados):
    catalogo = Catalogo(**dados)
    assert {e.coletor for e in catalogo.evidencias} == set(COLETORES)


def test_sinais_de_texto_tem_uso(dados):
    """Todo sinal de texto extraído vira evidência ou indicador de combinação."""
    from typing import get_args

    from app.modelos.extracao import SinalTexto

    catalogo = Catalogo(**dados)
    usados = {e.id for e in catalogo.evidencias}
    usados |= {i.extracao.split(".")[1] for c in catalogo.combinacoes for i in c.indicadores if i.extracao}
    if "pedido_sigilo" in usados:
        usados.add("sigilo")
    faltando = set(get_args(SinalTexto.model_fields["tipo"].annotation)) - usados
    assert not faltando


def test_recusa_coletor_desconhecido(dados):
    d = copy.deepcopy(dados)
    d["evidencias"][0]["coletor"] = "inexistente"
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_caminho_extracao_invalido(dados):
    d = copy.deepcopy(dados)
    d["combinacoes"][0]["indicadores"][2]["extracao"] = "beneficios.piscina"
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_faixas_fora_de_ordem(dados):
    d = copy.deepcopy(dados)
    d["faixas"]["alto_risco_ate"] = 80
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_bonus_fora_de_ordem(dados):
    d = copy.deepcopy(dados)
    d["combinacoes"][0]["bonus"] = [{"minimo": 3, "pontos": -20}, {"minimo": 2, "pontos": -10}]
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_risco_com_pontos_positivos(dados):
    d = copy.deepcopy(dados)
    d["evidencias"][0]["pontos"] = 10
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_condicao_indefinida(dados):
    d = copy.deepcopy(dados)
    d["evidencias"][0]["aplica_quando"] = ["nao_existe"]
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_id_repetido(dados):
    d = copy.deepcopy(dados)
    d["evidencias"].append(copy.deepcopy(d["evidencias"][0]))
    with pytest.raises(ValidationError):
        Catalogo(**d)


@pytest.mark.parametrize(
    "caminho,esperado",
    [
        ("beneficios.alojamento", True),
        ("sinais_texto.publico_migrante", True),
        ("beneficios.piscina", False),
        ("inexistente.alojamento", False),
        ("cargo.valor", False),
    ],
)
def test_caminho_extracao(caminho, esperado):
    assert caminho_extracao_valido(caminho) is esperado
