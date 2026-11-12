"""Formato das fontes e dos casos usados para testar e calibrar o motor.

Nada daqui é consultado durante a análise de uma oferta. Os casos servem para
medir acertos e falsos positivos e para ajustar os pesos do catálogo.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from .base import Base, Camada, Faixa

UsoFonte = Literal["padroes", "casos_de_risco", "casos_legitimos", "falsos_positivos", "sinais_estruturais", "rotas"]

# principal: fonte brasileira que mede o motor no contexto real do público.
# apoio: fonte útil, mas de outro contexto ou com um caso só; nunca é a métrica principal.
PapelFonte = Literal["principal", "apoio"]


class FonteCalibracao(Base):
    """Uma base ou documento de onde saem casos ou padrões de teste."""

    id: str = Field(pattern=r"^[a-z0-9_]+$")
    nome: str
    responsavel: str
    descricao: str
    referencias: list[str] = Field(min_length=1)
    idioma: Literal["pt", "en"]
    camadas: list[Camada] = Field(min_length=1)
    papel: PapelFonte
    usos: list[UsoFonte] = Field(min_length=1)
    licenca: str
    # Se o texto original pode ir para o repositório. Quando é falso, os casos
    # com texto original ficam em calibracao/casos/locais/, fora do git.
    redistribuir: bool


class Esperado(Base):
    """O que o motor deve devolver para o caso."""

    faixas: list[Faixa] = Field(min_length=1)
    alerta_aliciamento: bool
    # Evidências que precisam aparecer. Outras podem aparecer também.
    evidencias: list[str] = []


class CasoCalibracao(Base):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    fonte: str
    # original: texto como foi publicado; traducao: tradução de um original;
    # sintetico: escrito pela equipe a partir dos padrões de uma fonte.
    tipo_texto: Literal["original", "traducao", "sintetico"]
    rotulo: Literal["golpe", "aliciamento", "legitima"]
    texto: str = Field(min_length=20)
    municipio_pessoa: Optional[str] = Field(default=None, description="Município do perfil, no formato Cidade/UF")
    observacao: Optional[str] = None
    esperado: Esperado

    @model_validator(mode="after")
    def _coerencia_do_rotulo(self) -> "CasoCalibracao":
        if self.rotulo == "aliciamento" and not self.esperado.alerta_aliciamento:
            raise ValueError("caso de aliciamento precisa esperar o alerta de aliciamento")
        if self.rotulo == "legitima":
            if self.esperado.alerta_aliciamento:
                raise ValueError("caso legítimo não pode esperar o alerta de aliciamento")
            if "sinais_fortes" in self.esperado.faixas:
                raise ValueError("caso legítimo não pode aceitar a faixa sinais_fortes")
        return self
