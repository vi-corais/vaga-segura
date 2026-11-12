# Calibração e testes do motor

Esta pasta guarda as fontes e os casos usados para medir o motor e ajustar os pesos do [catálogo](../catalogo/evidencias.yaml). Nada daqui é consultado durante a análise de uma oferta: as bases consultadas estão em [bases-de-dados.md](../docs/arquitetura/bases-de-dados.md).

| Arquivo | Conteúdo |
|---|---|
| `fontes.yaml` | De onde vêm os casos e os padrões, com licença e uso permitido |
| `casos/*.yaml` | Casos que podem ir para o repositório (sintéticos ou de fonte que permite redistribuição) |
| `casos/locais/` | Casos com texto original de terceiros que não pode ser redistribuído. Fica fora do git |

O formato está em [`app/modelos/calibracao.py`](../app/modelos/calibracao.py), e `tests/test_calibracao.py` confere se cada caso usa uma fonte registrada, se as evidências esperadas existem no catálogo e se o texto original de fonte restrita ficou fora do repositório.

## Fontes

As fontes têm dois papéis. As **principais** são brasileiras e medem o motor no contexto real do público. As de **apoio** são úteis, mas vêm de outro contexto ou têm um caso só, e nunca entram como métrica principal.

| Fonte | Papel | Camada | O que mede |
|---|---|---|---|
| Sine BH (Prefeitura de Belo Horizonte) | Principal | Ambas | Falsos positivos do motor inteiro, com CNPJ, cargo e salário reais |
| Comunicados de resgate do MTE e do MPT | Principal | Gravidade | Padrões reais de aliciamento |
| Perfil Resgatado (Repórter Brasil) | Principal | Gravidade | Rotas de origem e destino do coletor `rota` e do mapa de risco |
| Alertas da Febraban e dos Procons | Principal | Geral | Golpes de hoje: código do SMS, dados bancários, golpe da tarefa |
| Ofertas doadas pelo público | Principal | Ambas | O formato exato que o bot recebe |
| EMSCAD | Apoio | Geral | Falsos positivos das regras de texto |
| Operação Fake Job | Apoio | Geral | Padrão histórico e cobertura do catálogo |
| Casos da equipe | Apoio | Ambas | O que as outras fontes não trazem |

### Sine BH

A Prefeitura de Belo Horizonte publica, a cada trimestre, as vagas cadastradas e ofertadas pela Central de Vagas do Sine BH, sob licença CC BY. Cada linha tem data, CNPJ, ocupação, local de trabalho, número de vagas, experiência, escolaridade e remuneração.

É a fonte mais importante da calibração. Por serem vagas intermediadas por um serviço público, o rótulo de vaga legítima é confiável. Como trazem CNPJ e salário, dá para rodar os coletores de Receita, salário e coerência em empresas reais e medir se o motor acusa quem é honesto. O EMSCAD não permite isso.

Limites: só Belo Horizonte, e sem texto livre. A mensagem do caso é montada a partir dos campos (por exemplo, "Vaga de repositor, R$ 1.700, empresa CNPJ tal") e marcada como `tipo_texto: sintetico`, mas os dados conferidos são reais.

### Comunicados de resgate do MTE e do MPT

Notícias oficiais de operações de resgate que contam como os trabalhadores foram recrutados: estado de origem, promessa de salário, transporte e alojamento, viagem cobrada, acordo só verbal. Hoje são a única fonte com padrões reais da camada de gravidade. Os casos são escritos pela equipe a partir dos padrões, sem nomes de trabalhadores, e citam o comunicado na observação.

### Perfil Resgatado

Levantamento da Repórter Brasil que cruza três bases do MTE e mostra os fluxos de origem e destino dos trabalhadores resgatados desde 1995. Não gera casos de texto: serve para conferir se o coletor `rota` e o mapa de risco marcam as rotas que aparecem nos resgates reais. A publicação é protegida por direitos autorais, então usamos só números agregados com citação, ou pedimos os dados à Repórter Brasil, o que também abre espaço para uma parceria.

### Alertas da Febraban e dos Procons

Alertas públicos sobre os golpes atuais, que as fontes antigas não cobrem: falso recrutador, pedido do código que chega por SMS, dados bancários, golpe da tarefa e conta laranja. Os casos são sintéticos e citam o alerta de origem.

### Ofertas doadas pelo público

Mensagens e prints que as pessoas receberam e aceitaram compartilhar nas conversas de validação. São o formato exato que o bot vai receber e valem mais que qualquer base pronta. Antes de registrar, tirar nome, telefone e qualquer dado de quem recebeu. Ficam em `casos/locais/`, fora do repositório. O rótulo é dado por quem não escreveu as regras do catálogo, para evitar que os casos já nasçam ajustados às regras.

### EMSCAD (apoio)

Base pública da Universidade do Egeu com 17.880 anúncios reais publicados na plataforma Workable entre 2012 e 2014, dos quais 866 foram marcados como fraudulentos pela equipe da plataforma. Usamos as vagas legítimas para medir falsos positivos das regras de texto e os indicadores da base (sem perfil da empresa, sem logotipo) para conferir os pesos das evidências de ausência.

Limites: é em inglês, de outro mercado e anterior ao PIX e ao golpe da tarefa. São anúncios de plataforma, não mensagens. O rótulo veio do comportamento da conta, e não do texto. Não mede os coletores de dados públicos nem a camada de gravidade. O artigo não informa licença para os dados, então os textos não vão para o repositório.

### Operação Fake Job (apoio)

Caso brasileiro de golpe do falso emprego investigado pela Polícia Civil do DF e denunciado pela Promotoria de Defesa do Consumidor do MPDFT em 2016. O grupo atuou de 2013 a 2016. É um caso só e anterior ao PIX, por isso serve como padrão histórico e para conferir a cobertura do catálogo. Não guardamos nomes de pessoas investigadas nem relatos identificáveis de vítimas.

| Padrão do caso | Evidência no catálogo | Situação |
|---|---|---|
| Curso ou certidão pagos como condição para a vaga (R$ 150 a R$ 250) | `cobranca_antecipada` | Coberto |
| Pressa para pagar e garantir a vaga | `urgencia` | Coberto |
| Pagamento para o site do curso, e não para a empresa | `pix_para_terceiro` (quando é por PIX) | Coberto em parte |
| Sites novos criados quando os antigos acumulavam denúncias | `dominio_recente` | Coberto |
| Contato por telefone a partir de currículos, sem candidatura | `abordagem_nao_solicitada` | Lacuna: previsto na fase 2 do [roteiro](../docs/roteiro.md) |
| "Encaminhamento" para empresas que não tinham a vaga | (nenhuma) | Fora do alcance: exigiria confirmar com a empresa |

### Casos escritos pela equipe (apoio)

Ofertas montadas pela equipe para cobrir o que as outras fontes não trazem. Sempre marcadas como `tipo_texto: sintetico`.

## Cuidados de método

- **Separar ajuste de avaliação.** Os casos usados para ajustar os pesos não entram na métrica publicada. Antes de calibrar, separamos uma parte de cada fonte só para avaliação.
- **Quem rotula não escreve as regras.** Os casos de avaliação são escritos ou rotulados por quem não mexeu no catálogo.
- **Métrica por fonte e por camada, com o limite ao lado.** Por exemplo: "falsos positivos do motor em vagas do Sine BH", e não "precisão do sistema".

## Formato de um caso

```yaml
casos:
  - id: fake_job_curso_obrigatorio      # único, minúsculas e _
    fonte: operacao_fake_job            # id de fontes.yaml
    tipo_texto: sintetico               # original, traducao ou sintetico
    rotulo: golpe                       # golpe, aliciamento ou legitima
    municipio_pessoa: Maceió/AL         # opcional, simula o perfil
    texto: >-
      ...
    esperado:
      faixas: [sinais_fortes, atencao]  # faixas aceitas
      alerta_aliciamento: false
      evidencias: [cobranca_antecipada] # precisam aparecer; outras podem aparecer
```

Regras:

- Domínios, e-mails e telefones dos casos sintéticos usam `.example` ou números fictícios, para não apontar para ninguém real.
- Casos de golpe e de aliciamento esperam pelo menos uma evidência de risco. Casos legítimos só podem esperar evidências de confiança e nunca aceitam a faixa `sinais_fortes`.
- Métricas são publicadas separadas por fonte e por camada, e sempre com o limite da fonte ao lado.
