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

COLETORES = ("cnpj", "listas_mte", "sancoes", "salario", "coerencia", "rota", "contato", "texto")
Coletor = Literal["cnpj", "listas_mte", "sancoes", "salario", "coerencia", "rota", "contato", "texto"]

Faixa = Literal["sinais_fortes", "atencao", "sem_sinais_relevantes", "inconclusivo"]

# Camada 1 (geral): golpes de falso emprego em qualquer vaga.
# Camada 2 (gravidade): aliciamento para trabalho análogo à escravidão.
# "ambas": evidência que serve aos dois tipos de risco.
Camada = Literal["geral", "gravidade", "ambas"]

# presenca: algo que a oferta diz ou tem. contradicao: um dado desmente outro
# (ex.: domínio de outra empresa). ausencia: falta algo esperado. Ausência nunca é forte.
Natureza = Literal["presenca", "contradicao", "ausencia"]

# Agrupa as evidências por tipo de problema. O resultado lista as categorias
# encontradas, e a explicação usa isso para escolher orientações e canais.
Categoria = Literal[
    "empresa",
    "contato_e_links",
    "dinheiro",
    "dados_pessoais",
    "tarefa",
    "abordagem",
    "condicoes_trabalho",
    "deslocamento",
    "listas_oficiais",
]
