"""Contrato 2: evidências geradas pelos coletores e resultado final da análise.

Todo coletor implementa:

    async def coletar(extracao: ExtracaoOferta, norm: Normalizacao) -> ResultadoColetor

Falha de fonte NUNCA vira risco: vira Verificacao(status="falhou").
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


Direcao = Literal["risco", "confianca"]
Forca = Literal["forte", "moderada", "fraca"]


class Evidencia(Base):
    """Um fato verificado, com fonte e pontos. Os pontos vêm do catálogo, não do coletor."""

    id: str = Field(description="Igual a um id de catalogo/evidencias.yaml")
    coletor: str = Field(description="Ex.: 'cnpj', 'listas_mte', 'salario'")
    direcao: Direcao
    forca: Forca
    pontos: int = Field(description="Copiado do catálogo pelo motor")
    confianca_coleta: float = Field(1.0, ge=0, le=1, description="Qualidade do dado obtido (ex.: match aproximado < 1)")
    fonte: str = Field(description="Ex.: 'Cadastro de Empregadores MTE'")
    fonte_data: Optional[date] = Field(None, description="Data de referência da fonte")
    trecho: Optional[str] = Field(None, description="Trecho da oferta relacionado, se houver")
    valor_observado: Optional[str] = Field(None, description="Ex.: 'R$ 4.500/mês'")
    referencia: Optional[str] = Field(None, description="Ex.: 'mediana local R$ 1.680'")
    base_legal: list[str] = []


class Verificacao(Base):
    """Registro de cada checagem tentada. É a base do cálculo de cobertura."""

    coletor: str
    status: Literal["concluida", "nao_aplicavel", "falhou", "sem_dados"]
    motivo: Optional[str] = None
    duracao_ms: Optional[int] = Field(None, ge=0)


class ResultadoColetor(Base):
    verificacoes: list[Verificacao]
    evidencias: list[Evidencia] = []


# Resultado final (etapas 4 a 6)

Faixa = Literal["alto_risco", "atencao", "sem_sinais_relevantes", "inconclusivo"]


class ItemExplicacao(Base):
    evidencia_id: str = Field(description="O guardrail rejeita item sem evidência correspondente")
    texto: str


class Canal(Base):
    nome: str
    url: Optional[str] = None
    telefone: Optional[str] = None


class Explicacao(Base):
    resumo: str
    itens: list[ItemExplicacao]
    perguntas_recrutador: list[str] = []
    orientacoes: list[str] = []
    canais: list[Canal] = []


class ResultadoAnalise(Base):
    analise_id: UUID
    criado_em: datetime
    versao_catalogo: str
    versao_esquema: str
    pontuacao: int = Field(ge=0, le=100)
    faixa: Faixa
    cobertura: float = Field(ge=0, le=1)
    tetos_aplicados: list[str] = Field([], description="Ids das evidências que aplicaram teto")
    bonus_combinacao: int = 0
    evidencias: list[Evidencia]
    verificacoes: list[Verificacao]
    explicacao: Explicacao
