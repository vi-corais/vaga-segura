# Como contribuir

Obrigado pelo interesse no Vaga Segura. O projeto é aberto a contribuições de código, de dados, de revisão jurídica e de documentação. Este guia explica como o trabalho é organizado e o que esperamos de cada contribuição.

Ao participar, você concorda com o [código de conduta](CODE_OF_CONDUCT.md).

> Este repositório não recebe denúncias. Se você recebeu uma oferta suspeita, procure seu banco (e o MED, se pagou por PIX) e registre boletim de ocorrência. Em caso de suspeita de trabalho escravo, denuncie pelo [Sistema Ipê](https://ipe.sit.trabalho.gov.br/) ou pelo Disque 100.

## Formas de contribuir

|Tipo|Exemplos|
|---|---|
|Sinais e evidências|Propor uma evidência nova para o catálogo, rever um peso, apontar a base legal de um sinal|
|Calibração|Sugerir fontes públicas de vagas legítimas ou de golpes, escrever casos sintéticos a partir de comunicados oficiais|
|Jurídico|Revisar [`docs/referencias/juridico.md`](docs/referencias/juridico.md), a linguagem do resultado e os cuidados com a LGPD|
|Código|Coletores, motor, extração, API e canais, seguindo os contratos em [`docs/arquitetura/contratos.md`](docs/arquitetura/contratos.md)|
|Documentação|Correções, clareza, exemplos|

Para mudanças grandes, abra primeiro uma issue para discutir a ideia. Para correções pequenas, pode ir direto ao pull request.

## Fluxo de branches

Usamos uma versão simplificada do Git Flow.

|Branch|Para que serve|Quem escreve|
|---|---|---|
|`main`|Versão publicada e estável. É o que aparece para quem visita o repositório|Só recebe merge de `develop` (ou de `hotfix/*`) por pull request|
|`develop`|Integração do trabalho em andamento|Recebe os pull requests das branches de trabalho|
|`feature/<area>-<descricao>`|Funcionalidade nova. Ex.: `feature/coletor-cnpj`, `feature/motor-faixas`|Sai de `develop`, volta para `develop`|
|`fix/<descricao>`|Correção de algo que já está em `develop`|Sai de `develop`, volta para `develop`|
|`docs/<descricao>`|Só documentação. Ex.: `docs/juridico-lgpd`|Sai de `develop`, volta para `develop`|
|`catalogo/<descricao>`|Mudança de pesos, tetos ou evidências do catálogo|Sai de `develop`, volta para `develop`|
|`hotfix/<descricao>`|Correção urgente no que já está em `main`|Sai de `main`, volta para `main` e para `develop`|

Regras:

- Ninguém envia commits direto para `main` ou `develop`. Todo trabalho entra por pull request.
- Nomes de branch em minúsculas, sem acento, com hífen: `feature/coletor-listas-mte`.
- Uma branch trata de um assunto só. Se o assunto crescer, divida em mais de um pull request.
- Mantenha a sua branch atualizada com `develop` antes de pedir revisão.
- A branch é apagada depois do merge.

Passo a passo:

```bash
git switch develop
git pull
git switch -c feature/coletor-cnpj
# ... trabalho e commits ...
git push -u origin feature/coletor-cnpj
```

Depois, abra o pull request para `develop` no GitHub.

## Commits

As mensagens de commit são em português, no presente, começando pelo verbo na terceira pessoa, e dizem o que o commit faz:

```
Adiciona o coletor de CNPJ com cache da BrasilAPI
Corrige o teto da camada geral no catálogo
Atualiza as referências jurídicas da LGPD
```

- Primeira linha com até 72 caracteres, sem ponto final.
- Se precisar explicar o porquê, deixe uma linha em branco e escreva o corpo.
- Faça commits pequenos e com sentido próprio. Evite "ajustes" ou "wip" no histórico final.
- Configure o git com o seu nome e e-mail antes do primeiro commit (`git config user.name` e `git config user.email`).

## Pull requests

- O destino é `develop`, exceto `hotfix/*` e a passagem de `develop` para `main`.
- Preencha o modelo que aparece ao abrir o pull request: o que muda, por quê, a issue ligada e o checklist.
- Todo pull request precisa da aprovação de pelo menos uma pessoa da equipe que não seja quem o abriu.
- Quem revisa comenta no próprio pull request. Quem abriu responde ou ajusta, e marca a conversa como resolvida.
- O merge para `develop` é feito com **squash**, para que cada pull request vire um commit com a mensagem no padrão acima. A passagem de `develop` para `main` usa **merge commit**, para preservar o histórico.

## Regras do projeto

Essas regras valem para qualquer contribuição, porque o projeto lida com pessoas vulneráveis, dados pessoais e acusações potencialmente graves.

### Dados e privacidade

- Nunca coloque no repositório o texto real de uma oferta recebida por terceiros, prints, nomes, telefones, e-mails, chaves PIX ou CPFs. Casos com texto real ficam em `calibracao/casos/locais/`, que está fora do git.
- Casos de calibração versionados são sintéticos ou vêm de fontes públicas que permitem redistribuição. Registre a fonte em [`calibracao/fontes.yaml`](calibracao/fontes.yaml).
- Nenhuma mudança pode passar a guardar o texto da oferta, os trechos extraídos ou os contatos que aparecem nela. Veja [`docs/arquitetura/modelo-de-dados.md`](docs/arquitetura/modelo-de-dados.md).
- Nunca envie o `.env`, chaves de API ou tokens. Use o [`.env.exemplo`](.env.exemplo) como referência.

### Catálogo de evidências

- Toda evidência nova ou peso alterado precisa de justificativa: base legal, fonte oficial ou resultado de calibração. Explique no pull request.
- Ao mudar o catálogo, suba o campo `versao` de [`catalogo/evidencias.yaml`](catalogo/evidencias.yaml).
- Cruzamentos feitos só por nome nunca geram risco forte.
- A IA não decide a pontuação. Regras novas ficam no catálogo, não em prompts.

### Linguagem do resultado

- O resultado aponta indícios; não acusa empresas nem pessoas.
- A melhor faixa é "sem sinais relevantes", nunca "vaga segura" ou "vaga confiável".
- A ferramenta faz triagem de indícios; não promete detectar trabalho escravo nem golpe.
- Textos para quem usa a ferramenta são em linguagem simples, pensados para quem tem pouca escolaridade.

### Contratos entre módulos

- Mudou um modelo em `app/modelos/`: suba `VERSAO_ESQUEMA` e rode `python scripts/gerar_schemas.py` para regravar `schemas/`.
- Mudou o catálogo: rode `python scripts/validar_catalogo.py`.

## Issues

Use os modelos disponíveis ao abrir uma issue: problema, proposta de evidência ou melhoria. Antes de abrir, procure se já existe uma parecida.

As labels `camada: geral` e `camada: gravidade` indicam a qual camada da análise a issue se refere. As demais indicam a área (`catalogo`, `calibracao`, `coletor`, `extracao`, `juridico`, `privacidade`).

## Segurança

Falhas de segurança ou de privacidade não devem ser abertas como issue pública. Veja a [política de segurança](SECURITY.md).

## Licença

Ao contribuir, você concorda que a sua contribuição será distribuída sob a [Licença Apache 2.0](LICENSE), a mesma do projeto.
