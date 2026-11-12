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
    d["faixas"]["sinais_fortes_ate"] = 80
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


def test_recusa_evidencia_sem_camada(dados):
    d = copy.deepcopy(dados)
    del d["evidencias"][0]["camada"]
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_ausencia_forte(dados):
    d = copy.deepcopy(dados)
    item = next(e for e in d["evidencias"] if e["natureza"] == "ausencia")
    item["forca"] = "forte"
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_recusa_alerta_com_combinacao_inexistente(dados):
    d = copy.deepcopy(dados)
    d["alerta_aliciamento"]["combinacoes"] = ["nao_existe"]
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_alerta_so_com_combinacao_de_gravidade(dados):
    d = copy.deepcopy(dados)
    d["combinacoes"][0]["camada"] = "geral"
    with pytest.raises(ValidationError):
        Catalogo(**d)


def test_duas_camadas_presentes(dados):
    """O catálogo cobre golpes em geral e a camada de gravidade."""
    camadas = {e.camada for e in Catalogo(**dados).evidencias}
    assert camadas == {"geral", "gravidade", "ambas"}


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


def test_indicadores_regionais_nao_ligam_alerta_sozinhos(dados):
    """Histórico da região não pode, sozinho, tratar a vaga como aliciamento."""
    catalogo = Catalogo(**dados)
    regional = next(e for e in catalogo.evidencias if e.id == "destino_setor_alto_risco")
    assert regional.forca not in catalogo.alerta_aliciamento.forcas
