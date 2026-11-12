# Bases de dados

As fontes estão separadas pela camada em que mais pesam. A camada geral cobre golpes de falso emprego em qualquer vaga; a camada de gravidade cobre o aliciamento para trabalho análogo à escravidão. Algumas fontes servem às duas.

## Fontes usadas no MVP

### Camada geral

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|CNPJ (Receita Federal)|Situação, data de abertura, CNAE, porte, capital social, endereço|Empresa recente, inativa, sem porte para a vaga ou com CNAE incoerente|Aberto (dados abertos)|
|CEIS / CNEP (CGU)|CNPJ, CPF|Empresa inidônea, suspensa ou punida|Aberto (API do Portal da Transparência)|
|Tabela CBO (MTE)|Código do cargo|Padroniza o cargo e permite cruzar com o CNAE|Aberto (download)|
|CNAE (IBGE/CONCLA)|Subclasse, divisão e seção da atividade econômica|Permite cruzar a atividade da empresa com o cargo e identificar setores de baixa presença digital|Aberto (download e API do IBGE)|
|Registro.br (RDAP)|Data de registro e CNPJ do titular do domínio .br|Site recém-criado ou titular diferente da empresa|Aberto (API)|
|Tabela de DDD (BrasilAPI)|DDD do telefone|DDD sem relação com a empresa ou com a vaga|Aberto (API)|
|Listas de phishing (Phishing.Database, URLhaus)|Links da mensagem e o destino dos links encurtados|Link malicioso|Aberto (listas públicas)|
|Google Safe Browsing (Update API)|Hash dos links da mensagem, conferido numa cópia local das listas|Link malicioso (phishing ou malware)|Gratuito só para uso não comercial; uso comercial exige o Web Risk|
|Expansão de links encurtados|Destino real de bit.ly, encurtador.com.br e similares, seguindo o redirecionamento no servidor sem abrir a página|Link encurtado ou que leva a outro domínio|Requisição HTTP do próprio servidor|
|Chaves PIX (regra local)|Formato e tipo da chave (CPF, CNPJ, e-mail, telefone, aleatória) e o documento da chave|Cobrança para CPF ou para CNPJ diferente da empresa|Regra local. O diretório do PIX (DICT) não é público|
|BrasilAPI|Interface única para CNPJ, CEP, DDD e Registro.br|Facilita o acesso às fontes públicas|Aberto (API de código aberto)|

### Camada de gravidade

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|QSA (Receita Federal)|Sócios do CNPJ|Sócio que consta na Lista Suja ou no CEAC|Aberto (dados abertos)|
|Lista Suja (MTE)|CNPJ, CPF, nome, município, CNAE|Empregador responsabilizado por trabalho escravo|Aberto (.txt e .xlsx)|
|CEAC (MTE)|CNPJ, CPF, nome|Empregador com termo de ajustamento de conduta (TAC)|Aberto (.xlsx)|
|Mapa de risco (derivado da Lista Suja)|Setor + município de destino|Região e setor com histórico de casos no Cadastro de Empregadores|Gerado por nós|
|IBGE Localidades|Municípios de origem e destino e a região geográfica imediata de cada um|Vaga fora do município ou fora da região imediata|Aberto (API)|

### As duas camadas

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|Novo CAGED (MTE)|Salário de admissão por cargo (CBO) e município|Salário muito acima ou abaixo do padrão local|Aberto (microdados)|
|Salário mínimo (Banco Central, SGS série 1619) e pisos estaduais|Valor vigente do mínimo nacional, fixado por decreto, e pisos das leis estaduais|Oferta abaixo do mínimo e descontos de moradia e alimentação acima do limite legal|Aberto (API do SGS). Os pisos estaduais vêm das leis de cada estado, numa tabela mantida por nós|

## Fontes públicas fora do MVP

|Fonte|Camada|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|---|
|SmartLab - Observatório da Erradicação do Trabalho Escravo (MPT/OIT)|Gravidade|Município de origem e de destino, setor econômico|Rota da oferta coincide com um fluxo histórico de aliciamento|Parcial: site aberto, mas sem download documentado. O site usa uma API interna sem documentação pública|
|Radar SIT (MTE)|Gravidade|Resgates por município e por atividade|Região e setor com histórico de resgates|Indisponível: fora do ar, com nova versão em construção, segundo comunicado da SIT|
|DNS do domínio (MX, SPF, DMARC)|Geral|Registros de e-mail do domínio citado|Domínio que não recebe e-mail ou é fácil de falsificar|Aberto (fase 2)|
|Consumidor.gov.br (Senacon)|Geral|Reclamações finalizadas por empresa, com CNPJ|Empresa com reclamações de cobrança indevida ou fraude|Aberto (dados abertos, fase 2). Alternativa legal ao Reclame Aqui|
|Lista de marcas imitadas|Geral|Nome, CNPJ raiz e domínios oficiais das marcas mais usadas em golpes|Oferta em nome de uma marca, com domínio, e-mail ou CNPJ que não são dela; domínio parecido com o oficial|Gerada por nós (fase 3). Como a base própria, depende de volume de uso e de revisão humana para não acusar revendedoras e terceirizadas|
|GLEIF (LEI)|Geral|Registro global de entidades legais|Confirma empresas de médio e grande porte|Aberto (API)|
|Google News (RSS)|Ambas|Nome da empresa e dos sócios + termos de risco|Menção a resgate ou golpe|Aberto (RSS)|
|Internet Archive|Geral|Histórico do site e do LinkedIn|Site ou perfil que surgiu junto com a vaga|Aberto (API)|
|Certificate Transparency (crt.sh)|Geral|Histórico de certificados do site|Domínio recém-ativado|Aberto (API)|
|ViaCEP / OpenStreetMap|Geral|Endereço da vaga e do CNPJ|Endereço inexistente ou divergente|Aberto (API)|

## Plataformas privadas (fora do MVP)

Sem API pública aberta ou com termos de uso restritivos. Ver o motivo em [escopo-mvp.md](../escopo-mvp.md). Na camada geral, Reclame Aqui e LinkedIn teriam peso maior do que na de gravidade, porque é neles que aparecem as queixas de vaga falsa, mas o problema dos termos de uso continua. A extensão de navegador da fase 2 lê só a página que a pessoa já abriu, sem raspar essas plataformas.

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|LinkedIn|Página da empresa, perfil do recrutador|Empresa ou recrutador inexistente, recém-criado ou divergente|Restrito: sem API aberta, só busca na web + Internet Archive|
|Reclame Aqui|Reputação e reclamações|Queixas de golpe ou de vaga falsa|Restrito: sem API pública e com termos de uso restritivos|
|Indeed|Vaga por empresa e data|Mesma vaga publicada pela mesma empresa|Restrito: sem API pública aberta|
|Glassdoor|Avaliações da empresa|Empresa sem histórico ou mal avaliada|Restrito: sem API pública aberta|
|Gupy|Vaga por cargo e empresa|Vaga confirmada no canal oficial|Parcial: API interna sem documentação|
|Catho / Vagas.com / InfoJobs|Vaga por empresa e data|Vaga confirmada ou texto replicado|A verificar|

## Bases de teste e calibração

Não são consultadas durante a análise. Servem para medir acertos e falsos positivos e para ajustar os pesos do catálogo. Os detalhes, as licenças e o formato dos casos estão em [`calibracao/`](../../calibracao/README.md).

|Fonte|Papel|O que traz|Uso|Limite|
|---|---|---|---|---|
|Sine BH (Prefeitura de Belo Horizonte)|Principal|Vagas reais intermediadas pelo Sine, com CNPJ, ocupação, local, remuneração, experiência e escolaridade (CC BY)|Medir falsos positivos do motor inteiro em empresas reais|Só Belo Horizonte e sem texto livre: a mensagem é montada a partir dos campos|
|Comunicados de resgate do MTE e do MPT|Principal|Como os trabalhadores resgatados foram recrutados: origem, promessas, viagem cobrada, acordo verbal|Padrões e casos da camada de gravidade|Casos escritos pela equipe a partir dos relatos|
|Perfil Resgatado (Repórter Brasil)|Principal|Fluxos de origem e destino dos resgatados desde 1995, a partir de dados do MTE|Conferir o coletor `rota` e o mapa de risco|Publicação protegida: só números agregados com citação, ou dados pedidos à Repórter Brasil|
|Alertas da Febraban e dos Procons|Principal|Padrões dos golpes atuais (código do SMS, dados bancários, golpe da tarefa)|Casos da camada geral|Casos sintéticos|
|Ofertas doadas pelo público|Principal|Mensagens e prints reais, com consentimento|Casos no formato exato do bot|Ficam fora do repositório e sem dados de quem recebeu|
|EMSCAD (Universidade do Egeu)|Apoio|17.880 anúncios da plataforma Workable (2012 a 2014), 866 fraudulentos|Falsos positivos das regras de texto e pesos das evidências de ausência|Em inglês, de outro mercado, rótulo vindo do comportamento da conta. Licença dos dados não informada|
|Operação Fake Job (PCDF e MPDFT)|Apoio|Padrões de um golpe do falso emprego de 2013 a 2016|Padrão histórico e cobertura do catálogo|Um caso só, anterior ao PIX|

## Referências

- [MTE - Cadastro de Empregadores (Lista Suja) e CEAC](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo)
- [Cadastro de Empregadores em .txt](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/cadastro_de_empregadores.txt)
- [Portal da Transparência - sanções (CEIS e CNEP)](https://portaldatransparencia.gov.br/sancoes/consulta?cadastro=1)
- Novo CAGED - microdados no servidor FTP do PDET: `ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/` (o GitHub e os navegadores atuais não abrem links FTP; use um cliente FTP ou o ETL)
- [Banco Central - SGS, série 1619 (salário mínimo)](https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1?formato=json)
- [IBGE - API de localidades (municípios e regiões imediatas)](https://servicodados.ibge.gov.br/api/docs/localidades)
- [IBGE - CONCLA (tabelas da CNAE)](https://concla.ibge.gov.br/)
- [Registro.br - RDAP](https://rdap.registro.br/)
- [BrasilAPI](https://brasilapi.com.br/)
- [SmartLab - Observatório da Erradicação do Trabalho Escravo](https://smartlabbr.org/trabalhoescravo)
- [SmartLab no GitHub (código do site e da API)](https://github.com/smartlab-br)
- [Radar SIT - comunicado da Secretaria de Inspeção do Trabalho](https://sit.trabalho.gov.br/radar/)
- [Gupy - portal de vagas](https://portal.gupy.io/)
- [Google Safe Browsing - restrições de uso](https://developers.google.com/safe-browsing/v4/usage-limits)
- [Consumidor.gov.br](https://www.consumidor.gov.br/)
- [Prefeitura de Belo Horizonte - Vagas ofertadas pelo Sine BH (dados abertos)](https://dados.pbh.gov.br/dataset/vagas-ofertadas-pbh)
- [MTE - Notícias de resgates](https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo)
- [Repórter Brasil - Perfil Resgatado (Maranhão, 2025)](https://escravonempensar.org.br/wp-content/uploads/2025/05/PerfilResgatado_notatecnica_MA_web.pdf)
- [Vidros et al. (2017), Automatic Detection of Online Recruitment Frauds (EMSCAD), Future Internet](https://doi.org/10.3390/fi9010006)
- [Metrópoles - Operação Fake Job: MP denuncia sete por golpe contra desempregados (2016)](https://www.metropoles.com/distrito-federal/justica-distrito-federal/operacao-fake-job-mp-denuncia-sete-por-golpe-contra-desempregados)
