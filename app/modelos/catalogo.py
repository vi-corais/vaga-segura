"""Contrato 3: formato do catálogo de evidências (catalogo/evidencias.yaml).

O catálogo é a única fonte de pesos, tetos e base legal. O código do motor só lê.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Teto(Base):
    valor: int = Field(ge=0, le=100, description="Pontuação máxima quando a evidência está presente")
    quando: list[str] = Field([], description="Condições adicionais (todas precisam valer). Vazio = sempre")


class ItemCatalogo(Base):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    coletor: str
    direcao: Literal["risco", "confianca"]
    forca: Literal["forte", "moderada", "fraca"]
    pontos: int
    descricao: str
    texto_usuario: str = Field(description="Frase para o usuário; aceita {valor_observado} e {referencia}")
    base_legal: list[str] = []
    teto: Optional[Teto] = None
    neutralizar_em_setores_baixa_presenca: bool = False
    aplica_quando: list[str] = Field([], description="Condições para a evidência poder ser gerada (todas precisam valer)")
    criterio_match: Optional[list[str]] = Field(None, description="Tipos de cruzamento aceitos (regra contra homônimos)")

    @model_validator(mode="after")
    def sinal_coerente(self):
        if self.direcao == "risco" and self.pontos > 0:
            raise ValueError(f"{self.id}: evidência de risco precisa ter pontos <= 0")
        if self.direcao == "confianca" and self.pontos < 0:
            raise ValueError(f"{self.id}: evidência de confiança precisa ter pontos >= 0")
        if self.direcao == "confianca" and self.teto:
            raise ValueError(f"{self.id}: evidência de confiança não pode ter teto")
        return self


class IndicadorCombinacao(Base):
    id: str
    evidencia: Optional[str] = None
    extracao: Optional[str] = Field(None, description="Caminho na ExtracaoOferta, ex.: 'beneficios.alojamento'")
    quando: list[str] = Field([], description="Condições para o indicador contar (todas precisam valer)")

    @model_validator(mode="after")
    def uma_origem(self):
        if bool(self.evidencia) == bool(self.extracao):
            raise ValueError(f"{self.id}: informe 'evidencia' OU 'extracao'")
        return self


class BonusCombinacao(Base):
    minimo: int = Field(ge=2)
    pontos: int = Field(le=0)


class Combinacao(Base):
    id: str
    base_legal: list[str]
    indicadores: list[IndicadorCombinacao]
    bonus: list[BonusCombinacao]


class Faixas(Base):
    alto_risco_ate: int
    atencao_ate: int
    cobertura_minima: float = Field(ge=0, le=1)
    inconclusivo_se_pontuacao_acima_de: int


class Catalogo(Base):
    versao: str
    pontuacao_base: int = Field(ge=0, le=100)
    teto_total_confianca: int = Field(ge=0)
    faixas: Faixas
    condicoes: dict[str, str] = Field({}, description="Condições usadas em teto.quando, aplica_quando e indicadores, com sua definição")
    setores_baixa_presenca_digital: dict[str, list[str]] = Field(
        description="Prefixos de CNAE (divisão) onde ausência de presença digital não pontua"
    )
    combinacoes: list[Combinacao]
    evidencias: list[ItemCatalogo]

    @model_validator(mode="after")
    def referencias_validas(self):
        ids = [e.id for e in self.evidencias]
        duplicados = {i for i in ids if ids.count(i) > 1}
        if duplicados:
            raise ValueError(f"ids duplicados: {duplicados}")
        for e in self.evidencias:
            for cond in (e.teto.quando if e.teto else []) + e.aplica_quando:
                if cond not in self.condicoes:
                    raise ValueError(f"{e.id}: condição não definida '{cond}'")
        for c in self.combinacoes:
            for ind in c.indicadores:
                if ind.evidencia and ind.evidencia not in ids:
                    raise ValueError(f"combinação {c.id}: evidência inexistente '{ind.evidencia}'")
                for cond in ind.quando:
                    if cond not in self.condicoes:
                        raise ValueError(f"combinação {c.id}: condição não definida '{cond}'")
        return self
