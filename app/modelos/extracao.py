"""Contrato 1: entrada da análise e saída da extração (etapa 1) e da normalização (etapa 2).

Regra central: todo valor informado pela IA carrega o trecho do texto original
que o justifica. Valor informado sem trecho é recusado pelo esquema, e o pipeline
descarta o campo cujo trecho não aparece no texto original. Campos com
"nao_informado" não precisam de trecho.
"""

from __future__ import annotations

from typing import Generic, Literal, Optional, TypeVar

from pydantic import Field, model_validator

from .base import PADRAO_UF, Base, CanalEntrada, Origem, RelacaoLocalidade

VERSAO_ESQUEMA = "0.3.0"

T = TypeVar("T")


# Entrada

class EntradaAnalise(Base):
    """O que o usuário envia. Também é entrada da normalização (município de origem)."""

    texto: str = Field(min_length=20, max_length=10_000, description="Texto da oferta ou texto extraído do print por OCR")
    origem: Origem = "texto"
    canal: CanalEntrada = "web"
    municipio_usuario_ibge: Optional[str] = Field(
        None, pattern=r"^\d{7}$", description="Município onde o usuário mora, vindo do perfil (código IBGE)"
    )


# Etapa 1: extração (saída da IA, validada por este esquema)

class Campo(Base, Generic[T]):
    """Valor extraído + trecho literal do texto que o comprova."""

    valor: T
    trecho: str = Field(min_length=1, description="Cópia literal do trecho da oferta")


def _exigir_trecho(informado: bool, trecho: Optional[str], nome: str) -> None:
    if informado and not trecho:
        raise ValueError(f"{nome}: valor informado sem trecho")


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

    @model_validator(mode="after")
    def faixa_coerente(self):
        if self.valor_min is not None and self.valor_max is not None and self.valor_min > self.valor_max:
            raise ValueError("salario: valor_min maior que valor_max")
        return self


class LocalTrabalho(Base):
    municipio: Optional[str] = None
    uf: Optional[str] = Field(None, pattern=PADRAO_UF)
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
    """Forma de pagamento é o meio (dinheiro, PIX); pagamento por produção fica em Salario.periodo."""

    forma: Literal["especie", "pix", "deposito", "nao_informado"] = "nao_informado"
    momento: Literal["diario", "semanal", "quinzenal", "mensal", "ao_fim_do_servico", "nao_informado"] = Field(
        "nao_informado", description="'ao_fim_do_servico' quando só paga ao terminar a safra, a obra ou a empreitada"
    )
    duracao_servico_dias: Optional[int] = Field(None, ge=1, description="Duração prevista do serviço, se informada")
    trecho: Optional[str] = Field(None, description="Obrigatório quando algum campo for informado")

    @model_validator(mode="after")
    def trecho_quando_informado(self):
        informado = (
            self.forma != "nao_informado" or self.momento != "nao_informado" or self.duracao_servico_dias is not None
        )
        _exigir_trecho(informado, self.trecho, "pagamento")
        return self


class Contrato(Base):
    tipo: Literal["clt", "temporario", "pj", "diarista", "informal", "nao_informado"] = "nao_informado"
    trecho: Optional[str] = Field(None, description="Obrigatório quando o tipo for informado")
    jornada: Optional[Campo[str]] = None

    @model_validator(mode="after")
    def trecho_quando_informado(self):
        _exigir_trecho(self.tipo != "nao_informado", self.trecho, "contrato")
        return self


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
    canal_exclusivo_trecho: Optional[str] = Field(None, description="Obrigatório quando canal_exclusivo for informado")

    @model_validator(mode="after")
    def trecho_quando_informado(self):
        _exigir_trecho(self.canal_exclusivo != "nao_informado", self.canal_exclusivo_trecho, "canal_exclusivo")
        return self


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

    versao_esquema: Literal[VERSAO_ESQUEMA] = VERSAO_ESQUEMA  # type: ignore[valid-type]
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
    """Saída da etapa 2, calculada a partir de EntradaAnalise + ExtracaoOferta.

    É a entrada comum de todos os coletores.
    """

    # empresa
    cnpj: Optional[str] = Field(None, pattern=r"^\d{14}$", description="Só dígitos")
    cnpj_digitos_validos: Optional[bool] = None
    nome_empresa_normalizado: Optional[str] = Field(None, description="Sem acento, minúsculo, sem LTDA/ME/EIRELI")

    # cargo
    cbo_codigo: Optional[str] = Field(None, pattern=r"^\d{6}$")
    cbo_similaridade: Optional[float] = Field(None, ge=0, le=1)

    # geografia
    municipio_destino_ibge: Optional[str] = Field(None, pattern=r"^\d{7}$")
    uf_destino: Optional[str] = Field(None, pattern=PADRAO_UF)
    municipio_origem_ibge: Optional[str] = Field(
        None, pattern=r"^\d{7}$", description="Copiado de EntradaAnalise.municipio_usuario_ibge"
    )
    uf_origem: Optional[str] = Field(None, pattern=PADRAO_UF)
    regiao_imediata_origem: Optional[str] = Field(None, pattern=r"^\d{6}$")
    regiao_imediata_destino: Optional[str] = Field(None, pattern=r"^\d{6}$")
    relacao_localidade: RelacaoLocalidade = Field(
        "desconhecida", description="Pelas regiões geográficas imediatas do IBGE. 'nao_se_aplica' = trabalho remoto"
    )
    distancia_km: Optional[float] = Field(None, ge=0, description="Só para exibir ao usuário. Nenhuma regra usa distância")
    outra_uf: Optional[bool] = None

    # salário
    salario_mensal_estimado: Optional[float] = Field(None, ge=0)
    salario_minimo_referencia: Optional[float] = Field(None, ge=0, description="Mínimo nacional ou piso estadual vigente")

    # contatos
    dominios: list[str] = []
    email_pessoal: Optional[bool] = Field(None, description="gmail, hotmail, outlook etc.")
    ddds: list[str] = []
    documentos_pix: list[str] = Field([], description="CPF/CNPJ de chaves PIX, só dígitos")
