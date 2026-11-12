# Roteiro de evolução

|Fase|O que entra|
|---|---|
|1. MVP|O escopo definido em [escopo-mvp.md](escopo-mvp.md)|
|2. Alcance|Extensão de navegador (ver abaixo), transcrição de áudio no WhatsApp, parcerias de distribuição, recalibração com o uso real, novas evidências e bases da camada geral (ver abaixo) e, na camada de gravidade, integração com o SmartLab (fluxos de origem e destino dos trabalhadores resgatados) e com o novo Radar SIT, quando for lançado|
|3. Inteligência coletiva|Base própria (textos, telefones e chaves PIX repetidos em ofertas diferentes), lista de marcas imitadas e domínios parecidos, confirmação da vaga no site de carreiras oficial (Gupy e similares, se os termos de uso permitirem), relatos colaborativos com níveis de verificação e moderação, padrões de recrutadores recorrentes, calibração estatística (log-odds). Tudo isso depende de volume de uso e de uma equipe de revisão humana|
|4. Institucional|API e painel com dados agregados e anônimos para MPT, MTE e pesquisadores. Módulo de tráfico internacional (arts. 206 e 149-A do Código Penal) e versões em espanhol e crioulo haitiano para migrantes|
|5. Escala|Depende da aprovação do PL 1636. Oferecer o motor como implementação aberta do art. 8º, o sistema automatizado de indícios que as plataformas passariam a ser obrigadas a ter. Usar as fontes novas que o projeto cria (API de anúncios do art. 4º e lista de anunciantes notificados do art. 13)|

## Fase 2 em detalhe

### Extensão de navegador

Extensão para Chrome, Edge e Firefox, que é o formato padrão das ferramentas desse tipo (JobReaper e JobSentinel funcionam assim). Ela usa o mesmo motor, pela API do Vaga Segura, e não tem regras próprias.

- Botão "analisar" ao lado das vagas nos principais sites (Indeed, InfoJobs, Catho, Vagas.com, LinkedIn, Gupy e páginas de carreiras) e nos anúncios do Facebook e do Instagram.
- Clique direito sobre um texto selecionado, para ofertas recebidas por e-mail ou em grupos.
- Selo de risco no cartão da vaga, com o mesmo resultado e as mesmas evidências do WhatsApp e do site.
- Lê só a vaga que a pessoa pediu para analisar. Não guarda histórico de navegação nem envia páginas que não são de vagas.
- Não raspa as plataformas: o texto vem da página que a pessoa já abriu, o que evita o problema dos termos de uso.

### Novas evidências e bases da camada geral

|Tipo|Item|O que acrescenta|
|---|---|---|
|Evidência|`pagamento_cripto`|Pagamento ou cobrança em criptomoeda|
|Evidência|`marketing_multinivel`|Só comissão, "seja revendedor", ganho por indicar pessoas|
|Evidência|`vaga_publica_sem_concurso`|Vaga em órgão público ou estatal sem edital|
|Evidência|`pedido_compartilhamento`|Pede que a pessoa repasse a vaga para concluir a inscrição|
|Evidência|`sem_atribuicoes`|A oferta não diz o que a pessoa vai fazer|
|Evidência|`abordagem_nao_solicitada`|"Vimos seu currículo" sem candidatura|
|Evidência (confiança)|`link_site_carreiras`|Link para a página de vagas no domínio da empresa ou em ATS conhecido|
|Evidência (confiança)|`processo_seletivo_descrito`|As etapas da seleção estão descritas|
|Base|DNS do domínio (MX, SPF, DMARC)|Domínio que não recebe e-mail ou é fácil de falsificar|
|Base|[Consumidor.gov.br](https://www.consumidor.gov.br/) (dados abertos)|Reclamações por empresa, alternativa legal ao Reclame Aqui|
|Base|Certificate Transparency (crt.sh) e Internet Archive|Site recém-ativado ou que surgiu junto com a vaga|
|Base|ViaCEP e OpenStreetMap|Endereço inexistente ou divergente|
|Experiência|Cartão "avisar alguém"|Alerta para encaminhar no WhatsApp, sem o nome da empresa|
|Experiência|Perguntas de seguimento|A pessoa pergunta "por quê?" ou "o que eu faço?", e a resposta usa só as evidências|
|Experiência|Desfecho informado pelo usuário|"Era golpe?", anônimo, para recalibrar os pesos|

## Referências

- [PL 1636/2026 - ficha de tramitação](https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2613812)
- [PL 1636/2026 - inteiro teor](https://www.camara.leg.br/proposicoesWeb/prop_mostrarintegra?codteor=3109248&filename=PL%201636/2026)
- [SmartLab - Observatório da Erradicação do Trabalho Escravo e do Tráfico de Pessoas](https://smartlabbr.org/trabalhoescravo)
- [Radar SIT - Inspeção do Trabalho](https://sit.trabalho.gov.br/radar/)
- [Código Penal (compilado)](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm)
- [JobReaper - extensão de navegador para vagas](https://jobreaper.it/)
- [JobSentinel - detector de código aberto com extensão](https://jobsentinel.org/)
- [Consumidor.gov.br - boletim 2025 (dados abertos)](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/defesadoconsumidor/Biblioteca/boletins-1/boletim-consumidor-gov-br-2025-vfinal.pdf)
