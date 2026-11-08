"""Contrato 2: evidências geradas pelos coletores, pontuação e resultado final da análise.

Todo coletor implementa:

    async def coletar(extracao: ExtracaoOferta, norm: Normalizacao) -> ResultadoColetor

O coletor devolve só fatos (EvidenciaColetada). Direção, força e pontos vêm do
catálogo e são acrescentados pelo motor na etapa 4 (Evidencia).

Falha de fonte NUNCA vira risco: vira Verificacao(status="falhou").
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import Field, model_validator

from .base import Base, CanalEntrada, Coletor, Faixa, Origem, RelacaoLocalidade

Direcao = Literal["risco", "confianca"]
Forca = Literal["forte", "moderada", "fraca"]


# Etapa 3: saída dos coletores

class EvidenciaColetada(Base):
    """Um fato verificado, com fonte. Não tem pontos: quem pontua é o motor."""

    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Igual a um id de catalogo/evidencias.yaml")
    coletor: Coletor
    confianca_coleta: float = Field(1.0, ge=0, le=1, description="Qualidade do dado obtido (ex.: match aproximado < 1)")
    fonte: str = Field(description="Ex.: 'Cadastro de Empregadores MTE'")
    fonte_data: Optional[date] = Field(None, description="Data de referência da fonte")
    trecho: Optional[str] = Field(None, description="Trecho da oferta relacionado, se houver")
    valor_observado: Optional[str] = Field(None, description="Ex.: 'R$ 4.500/mês'")
    referencia: Optional[str] = Field(None, description="Ex.: 'mediana local R$ 1.680'")


class Verificacao(Base):
    """Registro de cada checagem tentada. É a base do cálculo de cobertura."""

    coletor: Coletor
    verificacao: str = Field(
        pattern=r"^[a-z0-9_]+$", description="Qual checagem do coletor (ex.: 'cnpj_situacao', 'lista_suja_qsa')"
    )
    status: Literal["concluida", "nao_aplicavel", "falhou", "sem_dados"]
    motivo: Optional[str] = None
    duracao_ms: Optional[int] = Field(None, ge=0)


class ResultadoColetor(Base):
    verificacoes: list[Verificacao] = Field(min_length=1)
    evidencias: list[EvidenciaColetada] = []

    @model_validator(mode="after")
    def verificacoes_unicas(self):
        chaves = [(v.coletor, v.verificacao) for v in self.verificacoes]
        if len(chaves) != len(set(chaves)):
            raise ValueError("verificação repetida no mesmo coletor")
        return self


# Etapa 4: pontuação

class Evidencia(EvidenciaColetada):
    """Evidência depois da etapa 4, com os dados do catálogo."""

    direcao: Direcao
    forca: Forca
    pontos: int = Field(description="Pontos do catálogo")
    pontos_aplicados: int = Field(
        description="Pontos depois de confianca_coleta e do ajuste de ausência por setor (0 quando neutralizada)"
    )
    base_legal: list[str] = []


class Pontuacao(Base):
    """Saída da etapa 4."""

    pontuacao_base: int = Field(ge=0, le=100)
    soma_evidencias: int = Field(description="Soma de pontos_aplicados, com o teto de confiança já aplicado")
    bonus_combinacao: int = Field(0, le=0, description="Maior bônus atingido; os bônus não acumulam")
    indicadores_combinacao: list[str] = Field([], description="Ids dos indicadores que contaram para o bônus")
    tetos_aplicados: list[str] = Field([], description="Ids das evidências cujo teto limitou a pontuação")
    pontuacao: int = Field(ge=0, le=100)
    evidencias: list[Evidencia]


class Classificacao(Base):
    """Saída da etapa 5."""

    cobertura: float = Field(ge=0, le=1, description="Verificações concluídas / verificações aplicáveis")
    faixa: Faixa


# Etapa 6: explicação e resultado final

class ItemExplicacao(Base):
    evidencia_id: str = Field(description="O guardrail rejeita item sem evidência correspondente")
    texto: str


class CanalDenuncia(Base):
    nome: str
    url: Optional[str] = None
    telefone: Optional[str] = None


class Explicacao(Base):
    resumo: str
    itens: list[ItemExplicacao]
    perguntas_recrutador: list[str] = []
    orientacoes: list[str] = []
    canais: list[CanalDenuncia] = []


class ResultadoAnalise(Base):
    analise_id: UUID
    criado_em: datetime
    versao_catalogo: str
    versao_esquema: str
    modelo_ia: str = Field(description="Ex.: 'qwen3:8b-q4_K_M'")
    origem: Origem
    canal: CanalEntrada
    relacao_localidade: RelacaoLocalidade
    pontuacao: int = Field(ge=0, le=100)
    faixa: Faixa
    cobertura: float = Field(ge=0, le=1)
    tetos_aplicados: list[str] = Field([], description="Ids das evidências que aplicaram teto")
    bonus_combinacao: int = Field(0, le=0)
    evidencias: list[Evidencia]
    verificacoes: list[Verificacao]
    explicacao: Explicacao

    @model_validator(mode="after")
    def guardrail_explicacao(self):
        ids = {e.id for e in self.evidencias}
        orfaos = [i.evidencia_id for i in self.explicacao.itens if i.evidencia_id not in ids]
        if orfaos:
            raise ValueError(f"explicação cita evidências inexistentes: {orfaos}")
        return self
