"""Tipos e base comuns a todos os contratos."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    """Base dos contratos: campo fora do esquema é recusado."""

    model_config = ConfigDict(extra="forbid")


PADRAO_UF = r"^[A-Z]{2}$"

CanalEntrada = Literal["web", "whatsapp"]
Origem = Literal["texto", "imagem"]

RelacaoLocalidade = Literal[
    "mesmo_municipio", "mesma_regiao_imediata", "outra_regiao_imediata", "nao_se_aplica", "desconhecida"
]

COLETORES = ("cnpj", "listas_mte", "sancoes", "salario", "coerencia", "rota", "contato", "texto", "base_propria")
Coletor = Literal["cnpj", "listas_mte", "sancoes", "salario", "coerencia", "rota", "contato", "texto", "base_propria"]

Faixa = Literal["alto_risco", "atencao", "sem_sinais_relevantes", "inconclusivo"]
