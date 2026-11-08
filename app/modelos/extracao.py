"""Contrato 1: entrada da análise e saída da extração (etapa 1) e da normalização (etapa 2).

Regra central: todo dado extraído pela IA carrega o trecho do texto original
que o justifica. Campo sem trecho é descartado na validação.
"""

from __future__ import annotations

from typing import Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

VERSAO_ESQUEMA = "0.2.0"

T = TypeVar("T")


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


# Entrada

class EntradaAnalise(Base):
    """O que o usuário envia."""

    texto: str = Field(min_length=20, max_length=10_000, description="Texto da oferta ou texto extraído do print por OCR")
    origem: Literal["texto", "imagem"] = "texto"
    canal: Literal["web", "whatsapp"] = "web"
    municipio_usuario_ibge: Optional[str] = Field(
        None, pattern=r"^\d{7}$", description="Município onde o usuário mora, vindo do perfil (código IBGE)"
    )


# Etapa 1: extração (saída da IA, validada por este esquema)

class Campo(Base, Generic[T]):
    """Valor extraído + trecho literal do texto que o comprova."""

    valor: T
    trecho: str = Field(min_length=1, description="Cópia literal do trecho da oferta")


class Empresa(Base):
    nome: Optional[Campo[str]] = None
    cnpj: Optional[Campo[str]] = Field(None, description="Como aparece no texto; a normalização valida os dígitos")


class Recrutador(Base):
    nome: Optional[Campo[str]] = None
    cargo_ou_papel: Optional[Campo[str]] = Field(None, description="Ex.: 'encarregado', 'gerente', 'RH'")


class Salario(Base):
    valor_min: Optional[float] = Field(None, ge=0)
    valor_max: Optional[float] = Field(None, ge=0)
    periodo: Literal["hora", "dia", "semana", "quinzena", "mes", "producao", "nao_informado"] = "nao_informado"
    trecho: str = Field(min_length=1)


class LocalTrabalho(Base):
    municipio: Optional[str] = None
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    zona_rural: Optional[bool] = None
    exterior: bool = False
    pais: Optional[str] = None
    modalidade: Literal["presencial", "remoto", "hibrido", "nao_informado"] = "nao_informado"
    trecho: str = Field(min_length=1)


class Beneficio(Base):
    tipo: Literal["alojamento", "transporte", "passagem", "alimentacao", "adiantamento", "outro"]
    pago_pelo_contratante: Optional[bool] = None
    trecho: str = Field(min_length=1)


class Cobranca(Base):
    """Qualquer valor que o trabalhador precisa pagar antes de começar."""

    tipo: Literal["taxa", "exame", "curso", "uniforme", "kit", "documentacao", "passagem", "outro"]
    valor: Optional[float] = Field(None, ge=0)
    trecho: str = Field(min_length=1)


class Desconto(Base):
    """Valor descontado do salário."""

    tipo: Literal["moradia", "alimentacao", "passagem", "transporte_diario", "ferramentas_epi", "outro"] = Field(
        description="'passagem' é a viagem até o local de trabalho; 'transporte_diario' é o vale-transporte"
    )
    valor: Optional[float] = Field(None, ge=0, description="Em reais por mês")
    percentual: Optional[float] = Field(None, ge=0, le=100, description="Percentual do salário, se a oferta disser")
    trecho: str = Field(min_length=1)


class Pagamento(Base):
    forma: Literal["especie", "pix", "deposito", "producao", "nao_informado"] = "nao_informado"
    momento: Literal["diario", "semanal", "quinzenal", "mensal", "ao_fim_do_servico", "nao_informado"] = Field(
        "nao_informado", description="'ao_fim_do_servico' quando só paga ao terminar a safra, a obra ou a empreitada"
    )
    duracao_servico_dias: Optional[int] = Field(None, ge=1, description="Duração prevista do serviço, se informada")
    trecho: Optional[str] = None


class Contrato(Base):
    tipo: Literal["clt", "temporario", "pj", "diarista", "informal", "nao_informado"] = "nao_informado"
    jornada: Optional[Campo[str]] = None


class ChavePix(Base):
    tipo: Literal["cpf", "cnpj", "telefone", "email", "aleatoria", "desconhecido"]
    valor: str
    trecho: str = Field(min_length=1)


class Contatos(Base):
    telefones: list[Campo[str]] = []
    emails: list[Campo[str]] = []
    links: list[Campo[str]] = []
    chaves_pix: list[ChavePix] = []
    canal_exclusivo: Literal["whatsapp", "telegram", "nenhum", "nao_informado"] = "nao_informado"


class SinalTexto(Base):
    tipo: Literal[
        "urgencia",  # "só hoje", "vagas acabando"
        "dispensa_requisitos",  # "sem experiência", "não precisa de documento"
        "ganho_garantido",  # "ganhe R$ X garantido"
        "pedido_documentos_originais",  # "traga sua carteira de trabalho e RG originais"
        "publico_migrante",  # direcionado a imigrantes ou recém-chegados
        "sigilo",  # "não comente com ninguém"
        "compra_estabelecimento_indicado",  # "as compras são feitas na cantina da fazenda"
    ]
    trecho: str = Field(min_length=1)


class ExtracaoOferta(Base):
    """Saída da etapa 1. É este esquema que vai como JSON Schema para o Ollama."""

    versao_esquema: Literal["0.2.0"] = VERSAO_ESQUEMA
    e_oferta_de_trabalho: bool = Field(description="Falso se o texto não for uma oferta de trabalho")
    empresa: Empresa = Empresa()
    recrutador: Recrutador = Recrutador()
    cargo: Optional[Campo[str]] = None
    quantidade_vagas: Optional[Campo[int]] = None
    salario: Optional[Salario] = None
    local_trabalho: Optional[LocalTrabalho] = None
    beneficios: list[Beneficio] = []
    cobrancas: list[Cobranca] = []
    descontos: list[Desconto] = []
    pagamento: Pagamento = Pagamento()
    contrato: Contrato = Contrato()
    contatos: Contatos = Contatos()
    sinais_texto: list[SinalTexto] = []


# Etapa 2: normalização (regras determinísticas, sem IA)

class Normalizacao(Base):
    """Saída da etapa 2. É a entrada comum de todos os coletores."""

    # empresa
    cnpj: Optional[str] = Field(None, pattern=r"^\d{14}$", description="Só dígitos")
    cnpj_digitos_validos: Optional[bool] = None
    nome_empresa_normalizado: Optional[str] = Field(None, description="Sem acento, minúsculo, sem LTDA/ME/EIRELI")

    # cargo
    cbo_codigo: Optional[str] = Field(None, pattern=r"^\d{6}$")
    cbo_similaridade: Optional[float] = Field(None, ge=0, le=1)

    # geografia
    municipio_destino_ibge: Optional[str] = Field(None, pattern=r"^\d{7}$")
    uf_destino: Optional[str] = None
    municipio_origem_ibge: Optional[str] = Field(None, pattern=r"^\d{7}$")
    uf_origem: Optional[str] = None
    regiao_imediata_origem: Optional[str] = Field(None, pattern=r"^\d{6}$")
    regiao_imediata_destino: Optional[str] = Field(None, pattern=r"^\d{6}$")
    relacao_localidade: Literal[
        "mesmo_municipio", "mesma_regiao_imediata", "outra_regiao_imediata", "nao_se_aplica", "desconhecida"
    ] = Field("desconhecida", description="Pelas regiões geográficas imediatas do IBGE. 'nao_se_aplica' = trabalho remoto")
    distancia_km: Optional[float] = Field(None, ge=0, description="Só para exibir. Nenhuma regra usa distância em km")
    outra_uf: Optional[bool] = None

    # salário
    salario_mensal_estimado: Optional[float] = Field(None, ge=0)
    salario_minimo_referencia: Optional[float] = Field(None, ge=0, description="Mínimo nacional ou piso estadual vigente")

    # contatos
    dominios: list[str] = []
    email_pessoal: Optional[bool] = Field(None, description="gmail, hotmail, outlook etc.")
    ddds: list[str] = []
    documentos_pix: list[str] = Field([], description="CPF/CNPJ de chaves PIX, só dígitos")
