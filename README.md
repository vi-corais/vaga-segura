# Vaga Segura

Ferramenta de código aberto que ajuda quem procura emprego a reconhecer sinais de vaga falsa ou golpe antes de aceitar uma oferta. Ela cruza a oferta com dados públicos brasileiros (Receita Federal, Cadastro de Empregadores do MTE, Novo CAGED, sanções da CGU) e usa IA local para ler o texto.

A análise tem duas camadas:

- **Camada geral:** golpes de falso emprego em qualquer vaga, como cobrança de taxa, golpe da tarefa, pedido de código ou de dados pessoais, links maliciosos e empresa que não existe ou não confere.
- **Camada de gravidade:** sinais de aliciamento para trabalho análogo à escravidão, como empregador na Lista Suja, transporte e alojamento pagos para outra região e adiantamento que vira dívida.

Projeto criado para o programa AI4Good da Brazil Conference 2027.

> O Vaga Segura aponta indícios a partir de dados públicos, em qualquer tipo de vaga. Ele não acusa empresas nem substitui a fiscalização. Em caso de golpe, procure seu banco (e o MED, se pagou por PIX) e registre boletim de ocorrência. Em caso de suspeita de trabalho escravo, denuncie pelo [Sistema Ipê](https://ipe.sit.trabalho.gov.br/) ou pelo Disque 100.

## Como funciona

1. A pessoa informa uma vez a cidade onde mora e depois encaminha a oferta pelo WhatsApp ou cola no site, em texto ou print.
2. Um modelo de linguagem rodando localmente extrai o que pode ser verificado: empresa, CNPJ, cargo, salário, local, benefícios, cobranças, contatos, links e pedidos (códigos, dados pessoais, depósitos).
3. Coletores consultam bases públicas: situação do CNPJ e sócios, sanções da CGU, salário do cargo na região e salário mínimo, domínio, links e contatos. Na camada de gravidade, também a Lista Suja e o CEAC e se a vaga leva a pessoa para fora do município ou da região.
4. Cada verificação gera evidências com peso definido no catálogo, e o motor calcula uma pontuação de confiança. Sinais da camada de gravidade ligam um alerta próprio, em qualquer faixa.
5. O resultado volta em linguagem simples, com as evidências, perguntas para fazer ao recrutador, orientações e os canais de denúncia certos para o tipo de golpe.

![Arquitetura](docs/arquitetura/arquitetura.excalidraw.png)

## Protótipo

As telas do aplicativo estão no [protótipo do Figma](https://www.figma.com/design/jJcYmtmqylbC4yp3gjg4xn/Vaga-Segura---Telas-do-aplicativo?node-id=0-1&t=VUD4snbejktUlezt-1): início, primeiro acesso (cidade onde a pessoa mora), verificação em andamento, resultado da análise, detalhe de cada indicador, histórico, canais de ajuda e dicas. O mesmo fluxo vale para o site e para o bot do WhatsApp.

## Status

O projeto está na fase de especificação. Os contratos entre os módulos, o catálogo de evidências, o esquema do banco e o formato dos casos de calibração estão prontos e são validados por testes, e as telas do aplicativo já estão no [protótipo](https://www.figma.com/design/jJcYmtmqylbC4yp3gjg4xn/Vaga-Segura---Telas-do-aplicativo?node-id=0-1&t=VUD4snbejktUlezt-1). Coletores, motor de cálculo, ETL, API e bot do WhatsApp estão em construção, na ordem definida no [escopo do MVP](docs/escopo-mvp.md#ordem-de-entrega).

## Estrutura

```
app/modelos/     contratos entre os módulos (Pydantic)
catalogo/        pesos, tetos e base legal das evidências
calibracao/      fontes e casos de teste para calibrar o motor
db/              esquema do banco (PostgreSQL 15+)
schemas/         JSON Schemas gerados a partir dos modelos
scripts/         geração dos schemas e validação do catálogo
tests/           testes dos contratos, do catálogo e dos casos
docs/            documentação do projeto
```

## Documentação

- [Resumo do projeto](docs/resumo.md)
- [Escopo do MVP](docs/escopo-mvp.md) e [roteiro de evolução](docs/roteiro.md)
- [Protótipo das telas](https://www.figma.com/design/jJcYmtmqylbC4yp3gjg4xn/Vaga-Segura---Telas-do-aplicativo?node-id=0-1&t=VUD4snbejktUlezt-1) (Figma)
- [Contratos entre os módulos](docs/arquitetura/contratos.md)
- [Bases de dados consultadas](docs/arquitetura/bases-de-dados.md)
- [Modelo de dados](docs/arquitetura/modelo-de-dados.md)
- [Calibração e testes do motor](calibracao/README.md): vagas reais do Sine BH, comunicados de resgate do MTE e do MPT, Perfil Resgatado, alertas de golpe e, como apoio, EMSCAD e Operação Fake Job
- [Referências jurídicas](docs/referencias/juridico.md) e [pesquisa](docs/referencias/pesquisa-pradhan-shehory-2026.md)

## Como contribuir

Contribuições de código, dados, revisão jurídica e documentação são bem-vindas. O trabalho segue um Git Flow simplificado: `main` guarda a versão publicada, `develop` integra o trabalho em andamento, e toda mudança entra por pull request, com revisão de outra pessoa da equipe.

- [Guia de contribuição](CONTRIBUTING.md): branches, commits, pull requests e as regras de privacidade, de catálogo e de linguagem do projeto
- [Código de conduta](CODE_OF_CONDUCT.md)
- [Política de segurança](SECURITY.md): falhas de segurança e de privacidade são relatadas de forma privada

Este repositório não recebe denúncias. Para isso, use os canais indicados no início desta página.

## Licença

Código sob a [Licença Apache 2.0](LICENSE). Os dados consultados pertencem às suas fontes; veja as [atribuições](ATRIBUICOES.md).
