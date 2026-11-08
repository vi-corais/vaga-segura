-- Vaga Segura: esquema do banco (PostgreSQL 15+)
-- Convenções:
--   * documentos (CNPJ/CPF) guardados só com dígitos
--   * colunas *_normalizado: minúsculas, sem acento, sem LTDA/ME/EIRELI (feito no ETL, em Python)
--   * nenhuma tabela guarda o texto original das ofertas (LGPD)

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 1. Controle de cargas (ETL)

CREATE TABLE fonte_carga (
    id              bigserial PRIMARY KEY,
    fonte           text        NOT NULL,  -- 'lista_suja', 'ceac', 'ceis', 'cnep', 'caged', 'cbo', 'ibge'...
    url_origem      text,
    data_referencia date,  -- data de atualização informada pela fonte
    carregado_em    timestamptz NOT NULL DEFAULT now(),
    linhas          integer,
    hash_arquivo    text  -- sha256 do arquivo baixado
);

-- 2. Tabelas de referência

CREATE TABLE municipios (
    codigo_ibge      char(7) PRIMARY KEY,
    nome             text    NOT NULL,
    nome_normalizado text    NOT NULL,
    uf               char(2) NOT NULL,
    regiao_imediata  char(6) NOT NULL,  -- Região Geográfica Imediata (IBGE)
    latitude         double precision,
    longitude        double precision
);
CREATE INDEX municipios_nome_trgm ON municipios USING gin (nome_normalizado gin_trgm_ops);

CREATE TABLE cbo_ocupacoes (
    codigo  char(6) PRIMARY KEY,
    titulo  text    NOT NULL,
    familia char(4) NOT NULL
);

CREATE TABLE cbo_sinonimos (
    codigo               char(6) NOT NULL REFERENCES cbo_ocupacoes (codigo),
    sinonimo             text    NOT NULL,
    sinonimo_normalizado text    NOT NULL,
    PRIMARY KEY (codigo, sinonimo_normalizado)
);
CREATE INDEX cbo_sinonimos_trgm ON cbo_sinonimos USING gin (sinonimo_normalizado gin_trgm_ops);

CREATE TABLE cnae_subclasses (
    codigo    char(7) PRIMARY KEY,  -- ex.: '0134200'
    descricao text    NOT NULL,
    divisao   char(2) NOT NULL,  -- 2 primeiros dígitos
    secao     char(1) NOT NULL
);

-- Quais famílias CBO cada divisão CNAE realmente contrata (derivado do CAGED)
CREATE TABLE cnae_cbo_compatibilidade (
    cnae_divisao char(2)  NOT NULL,
    cbo_familia  char(4)  NOT NULL,
    admissoes    integer  NOT NULL,
    proporcao    numeric(6,5) NOT NULL,  -- admissoes / total da divisão
    carga_id     bigint REFERENCES fonte_carga (id),
    PRIMARY KEY (cnae_divisao, cbo_familia)
);

-- Salário de admissão por cargo e região (agregado do Novo CAGED, últimos 12 meses)
CREATE TABLE salarios_cbo (
    cbo_codigo     char(6) NOT NULL,
    nivel          text    NOT NULL CHECK (nivel IN ('municipio', 'uf', 'brasil')),
    chave_geo      text    NOT NULL,  -- código IBGE, sigla da UF ou 'BR'
    n_admissoes    integer NOT NULL,
    p10            numeric(10,2) NOT NULL,
    p50            numeric(10,2) NOT NULL,
    p90            numeric(10,2) NOT NULL,
    periodo_inicio date    NOT NULL,
    periodo_fim    date    NOT NULL,
    carga_id       bigint REFERENCES fonte_carga (id),
    PRIMARY KEY (cbo_codigo, nivel, chave_geo)
);
-- O coletor usa 'municipio' se n_admissoes >= 30; senão cai para 'uf' e depois 'brasil'.

CREATE TABLE salario_minimo_pisos (
    id              serial PRIMARY KEY,
    uf              char(2),  -- NULL = salário mínimo nacional
    descricao       text    NOT NULL,  -- ex.: 'Piso regional SP - faixa 1'
    valor_mensal    numeric(10,2) NOT NULL,
    ato_normativo   text    NOT NULL,  -- ex.: 'Decreto 12.797/2025'
    fonte           text    NOT NULL CHECK (fonte IN ('bcb_sgs_1619', 'lei_estadual')),
    vigencia_inicio date    NOT NULL,
    vigencia_fim    date
);

-- 3. Cadastros oficiais (carregados pelo ETL)

-- Lista Suja e CEAC na mesma tabela, separados por 'cadastro'
CREATE TABLE empregadores_mte (
    id                bigserial PRIMARY KEY,
    cadastro          text    NOT NULL CHECK (cadastro IN ('lista_suja', 'ceac')),
    documento_tipo    text    NOT NULL CHECK (documento_tipo IN ('cnpj', 'cpf')),
    documento         text    NOT NULL,  -- só dígitos (CPF completo, nunca exibir)
    cnpj_raiz         char(8),  -- 8 primeiros dígitos, para pegar filiais
    nome              text    NOT NULL,
    nome_normalizado  text    NOT NULL,
    uf                char(2),
    municipio_ibge    char(7),
    estabelecimento   text,  -- endereço/descrição do local fiscalizado
    cnae              char(7),
    ano_acao_fiscal   smallint,
    trabalhadores     integer,
    data_inclusao     date,
    carga_id          bigint REFERENCES fonte_carga (id)
);
CREATE INDEX empregadores_mte_doc   ON empregadores_mte (documento);
CREATE INDEX empregadores_mte_raiz  ON empregadores_mte (cnpj_raiz);
CREATE INDEX empregadores_mte_nome  ON empregadores_mte USING gin (nome_normalizado gin_trgm_ops);

-- CEIS e CNEP (CGU)
CREATE TABLE sancoes (
    id                bigserial PRIMARY KEY,
    cadastro          text    NOT NULL CHECK (cadastro IN ('ceis', 'cnep')),
    documento_tipo    text    NOT NULL CHECK (documento_tipo IN ('cnpj', 'cpf')),
    documento         text    NOT NULL,
    nome              text    NOT NULL,
    nome_normalizado  text    NOT NULL,
    orgao_sancionador text,
    tipo_sancao       text,
    data_inicio       date,
    data_fim          date,  -- NULL = sem prazo final
    carga_id          bigint REFERENCES fonte_carga (id)
);
CREATE INDEX sancoes_doc ON sancoes (documento);

-- Casos por município e setor (derivado de empregadores_mte)
CREATE TABLE mapa_risco (
    municipio_ibge char(7) NOT NULL,
    cnae_divisao   char(2) NOT NULL,  -- '**' = todos os setores
    casos          integer NOT NULL,
    trabalhadores  integer NOT NULL,
    carga_id       bigint REFERENCES fonte_carga (id),
    PRIMARY KEY (municipio_ibge, cnae_divisao)
);

-- 4. Cache das consultas ao vivo (BrasilAPI, RDAP)

CREATE TABLE cache_consultas (
    fonte        text        NOT NULL,  -- 'brasilapi_cnpj', 'rdap_br'
    chave        text        NOT NULL,  -- CNPJ ou domínio
    resposta     jsonb,
    status_http  smallint,
    consultado_em timestamptz NOT NULL DEFAULT now(),
    expira_em    timestamptz NOT NULL,
    PRIMARY KEY (fonte, chave)
);
CREATE INDEX cache_consultas_expira ON cache_consultas (expira_em);

-- 5. Base própria (só impressões digitais, nunca o conteúdo)

-- Textos parecidos (MinHash)
CREATE TABLE base_textos (
    id            bigserial PRIMARY KEY,
    assinatura    bigint[]    NOT NULL,  -- assinatura MinHash (ex.: 128 valores)
    bandas_lsh    text[]      NOT NULL,  -- chaves LSH para busca rápida de similares
    primeiro_visto timestamptz NOT NULL DEFAULT now(),
    ultimo_visto  timestamptz NOT NULL DEFAULT now(),
    ocorrencias   integer     NOT NULL DEFAULT 1
);
CREATE INDEX base_textos_bandas ON base_textos USING gin (bandas_lsh);

-- Contato x empresa (detecta o mesmo contato por trás de "empresas" diferentes)
CREATE TABLE base_contatos (
    contato_tipo   text NOT NULL CHECK (contato_tipo IN ('telefone', 'pix', 'email')),
    contato_hash   text NOT NULL,  -- HMAC-SHA256 com segredo do servidor
    empresa_hash   text NOT NULL,  -- HMAC do CNPJ ou do nome normalizado; '' se não identificada
    primeiro_visto timestamptz NOT NULL DEFAULT now(),
    ultimo_visto   timestamptz NOT NULL DEFAULT now(),
    ocorrencias    integer     NOT NULL DEFAULT 1,
    PRIMARY KEY (contato_tipo, contato_hash, empresa_hash)
);

-- Perfil do usuário no WhatsApp: só o município, ligado ao HMAC do número.
-- No site, o perfil fica no navegador e não vem para o banco.
-- Apagado quando a pessoa pede ou depois de 12 meses sem uso.
CREATE TABLE perfis_usuario (
    contato_hash   text        PRIMARY KEY,  -- HMAC-SHA256 do número, mesmo segredo de base_contatos
    municipio_ibge char(7)     NOT NULL REFERENCES municipios (codigo_ibge),
    atualizado_em  timestamptz NOT NULL DEFAULT now()
);

-- 6. Auditoria das análises (sem texto, sem trechos, sem dados pessoais)

CREATE TABLE analises (
    id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    criada_em        timestamptz NOT NULL DEFAULT now(),
    versao_catalogo  text        NOT NULL,
    versao_esquema   text        NOT NULL,
    modelo_ia        text        NOT NULL,  -- ex.: 'qwen3:8b-q4_K_M'
    origem           text        NOT NULL CHECK (origem IN ('texto', 'imagem')),
    canal            text        NOT NULL CHECK (canal IN ('web', 'whatsapp')),
    pontuacao        smallint    NOT NULL CHECK (pontuacao BETWEEN 0 AND 100),
    faixa            text        NOT NULL CHECK (faixa IN ('alto_risco', 'atencao', 'sem_sinais_relevantes', 'inconclusivo')),
    cobertura        numeric(4,3) NOT NULL,
    bonus_combinacao smallint    NOT NULL DEFAULT 0,
    tetos_aplicados  text[]      NOT NULL DEFAULT '{}',
    uf_origem        char(2),  -- só UF, nunca município (agregação)
    uf_destino       char(2),
    relacao_localidade text  CHECK (relacao_localidade IN ('mesmo_municipio', 'mesma_regiao_imediata', 'outra_regiao_imediata', 'nao_se_aplica', 'desconhecida')),
    duracao_ms       integer
);
CREATE INDEX analises_criada_em ON analises (criada_em);

CREATE TABLE analise_evidencias (
    analise_id       uuid     NOT NULL REFERENCES analises (id) ON DELETE CASCADE,
    evidencia_id     text     NOT NULL,  -- id do catálogo
    pontos_aplicados smallint NOT NULL,
    confianca_coleta numeric(3,2) NOT NULL,
    PRIMARY KEY (analise_id, evidencia_id)
);

CREATE TABLE analise_verificacoes (
    analise_id uuid    NOT NULL REFERENCES analises (id) ON DELETE CASCADE,
    coletor    text    NOT NULL,
    status     text    NOT NULL CHECK (status IN ('concluida', 'nao_aplicavel', 'falhou', 'sem_dados')),
    duracao_ms integer,
    PRIMARY KEY (analise_id, coletor)
);
