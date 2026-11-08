"""Contrato 3: formato do catálogo de evidências (catalogo/evidencias.yaml).

O catálogo é a única fonte de pesos, tetos e base legal. O código do motor só lê.
"""

from __future__ import annotations

from typing import Literal, Optional, get_args

from pydantic import Field, model_validator

from .base import Base, Coletor
from .extracao import ExtracaoOferta

CriterioMatch = Literal["cnpj_exato", "cpf_exato", "socio_cpf_exato", "nome_municipio_cpf_parcial", "nome_aproximado"]


def caminho_extracao_valido(caminho: str) -> bool:
    """Confere caminhos como 'beneficios.alojamento': lista da ExtracaoOferta + valor do seu 'tipo'."""
    lista, _, tipo = caminho.partition(".")
    campo = ExtracaoOferta.model_fields.get(lista)
    if campo is None or not tipo:
        return False
    args = get_args(campo.annotation)
    if len(args) != 1:
        return False
    campos_item = getattr(args[0], "model_fields", {})
    if "tipo" not in campos_item:
        return False
    return tipo in get_args(campos_item["tipo"].annotation)


class Teto(Base):
    valor: int = Field(ge=0, le=100, description="Pontuação máxima quando a evidência está presente")
    quando: list[str] = Field([], description="Condições adicionais (todas precisam valer). Vazio = sempre")


class ItemCatalogo(Base):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    coletor: Coletor
    direcao: Literal["risco", "confianca"]
    forca: Literal["forte", "moderada", "fraca"]
    pontos: int
    descricao: str
    texto_usuario: str = Field(description="Frase para o usuário; aceita {valor_observado} e {referencia}")
    base_legal: list[str] = []
    teto: Optional[Teto] = None
    neutralizar_em_setores_baixa_presenca: bool = False
    aplica_quando: list[str] = Field([], description="Condições para a evidência poder ser gerada (todas precisam valer)")
    criterio_match: Optional[list[CriterioMatch]] = Field(
        None, description="Tipos de cruzamento aceitos (regra contra homônimos)"
    )

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
    extracao: Optional[str] = Field(
        None, pattern=r"^[a-z_]+\.[a-z_]+$", description="Lista da ExtracaoOferta + tipo, ex.: 'beneficios.alojamento'"
    )
    quando: list[str] = Field([], description="Condições para o indicador contar (todas precisam valer)")

    @model_validator(mode="after")
    def uma_origem(self):
        if bool(self.evidencia) == bool(self.extracao):
            raise ValueError(f"{self.id}: informe 'evidencia' OU 'extracao'")
        if self.extracao and not caminho_extracao_valido(self.extracao):
            raise ValueError(f"{self.id}: caminho de extração inexistente '{self.extracao}'")
        return self


class BonusCombinacao(Base):
    minimo: int = Field(ge=2, description="Quantidade mínima de indicadores presentes")
    pontos: int = Field(le=0)


class Combinacao(Base):
    """Bônus por indicadores que aparecem juntos. Vale só o maior bônus atingido (não acumulam)."""

    id: str
    base_legal: list[str]
    indicadores: list[IndicadorCombinacao] = Field(min_length=2)
    bonus: list[BonusCombinacao] = Field(min_length=1)

    @model_validator(mode="after")
    def bonus_crescentes(self):
        minimos = [b.minimo for b in self.bonus]
        pontos = [b.pontos for b in self.bonus]
        if minimos != sorted(set(minimos)):
            raise ValueError(f"combinação {self.id}: 'minimo' dos bônus precisa ser crescente e sem repetição")
        if any(a <= b for a, b in zip(pontos, pontos[1:])):
            raise ValueError(f"combinação {self.id}: cada bônus precisa ser maior (mais negativo) que o anterior")
        if minimos[-1] > len(self.indicadores):
            raise ValueError(f"combinação {self.id}: bônus exige mais indicadores do que existem")
        ids = [i.id for i in self.indicadores]
        if len(ids) != len(set(ids)):
            raise ValueError(f"combinação {self.id}: indicador repetido")
        return self


class Faixas(Base):
    """Faixas da pontuação (0 a 100).

    0 a alto_risco_ate = alto_risco; até atencao_ate = atencao; acima = sem_sinais_relevantes.
    Se a cobertura ficar abaixo de cobertura_minima e a pontuação passar de
    inconclusivo_se_pontuacao_acima_de, a faixa vira inconclusivo: verificamos pouco
    para dizer que não há sinais. Abaixo desse valor, a faixa de risco é mantida.
    """

    alto_risco_ate: int = Field(ge=0, le=100)
    atencao_ate: int = Field(ge=0, le=100)
    cobertura_minima: float = Field(ge=0, le=1)
    inconclusivo_se_pontuacao_acima_de: int = Field(ge=0, le=100)

    @model_validator(mode="after")
    def ordem(self):
        if not self.alto_risco_ate < self.atencao_ate < 100:
            raise ValueError("faixas: é preciso alto_risco_ate < atencao_ate < 100")
        return self


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
        for setor, divisoes in self.setores_baixa_presenca_digital.items():
            for d in divisoes:
                if len(d) != 2 or not d.isdigit():
                    raise ValueError(f"setor {setor}: divisão CNAE inválida '{d}'")
        return self
