"""Valida as fontes e os casos de calibração (calibracao/)."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from app.modelos.calibracao import CasoCalibracao, FonteCalibracao

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "calibracao"


def _yaml(caminho):
    with caminho.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def fontes():
    return {f.id: f for f in (FonteCalibracao(**d) for d in _yaml(PASTA / "fontes.yaml")["fontes"])}


@pytest.fixture(scope="module")
def evidencias():
    catalogo = _yaml(RAIZ / "catalogo" / "evidencias.yaml")
    return {e["id"]: e for e in catalogo["evidencias"]}


@pytest.fixture(scope="module")
def casos():
    # Os casos em casos/locais/ ficam fora do git, mas são validados quando existem.
    arquivos = sorted((PASTA / "casos").rglob("*.yaml"))
    return [CasoCalibracao(**d) for a in arquivos for d in (_yaml(a) or {}).get("casos", [])]


def test_ids_de_casos_unicos(casos):
    ids = [c.id for c in casos]
    assert len(ids) == len(set(ids))


def test_casos_usam_fontes_registradas(casos, fontes):
    assert {c.fonte for c in casos} <= set(fontes)


def test_texto_original_so_de_fonte_redistribuivel(casos, fontes):
    """Texto original de fonte que não pode ser redistribuída só fica em casos/locais/."""
    versionados = [
        CasoCalibracao(**d)
        for a in sorted((PASTA / "casos").glob("*.yaml"))
        for d in (_yaml(a) or {}).get("casos", [])
    ]
    for c in versionados:
        if c.tipo_texto in ("original", "traducao"):
            assert fontes[c.fonte].redistribuir, c.id


def test_evidencias_esperadas_existem_e_combinam_com_rotulo(casos, evidencias):
    for c in casos:
        for ev in c.esperado.evidencias:
            assert ev in evidencias, f"{c.id}: {ev} não está no catálogo"
        direcoes = {evidencias[ev]["direcao"] for ev in c.esperado.evidencias}
        if c.rotulo == "legitima":
            assert direcoes <= {"confianca"}, c.id
        else:
            assert "risco" in direcoes, c.id


def test_caso_de_aliciamento_exige_alerta():
    with pytest.raises(ValidationError):
        CasoCalibracao(
            id="x",
            fonte="equipe",
            tipo_texto="sintetico",
            rotulo="aliciamento",
            texto="Vaga na colheita com passagem e alojamento pagos.",
            esperado={"faixas": ["sinais_fortes"], "alerta_aliciamento": False},
        )


def test_cada_camada_tem_fonte_principal(fontes):
    """Geral e gravidade precisam de pelo menos uma fonte principal (brasileira)."""
    principais = [f for f in fontes.values() if f.papel == "principal"]
    for camada in ("geral", "gravidade"):
        assert any(camada in f.camadas for f in principais), camada
    assert all(f.idioma == "pt" for f in principais)
