# Bases de dados

## Fontes usadas no MVP

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|CNPJ (Receita Federal)|Situação, data de abertura, CNAE, porte, capital social, endereço|Empresa recente, inativa, sem porte para a vaga ou com CNAE incoerente|Aberto (dados abertos)|
|QSA (Receita Federal)|Sócios do CNPJ|Sócio que consta na Lista Suja ou no CEAC|Aberto (dados abertos)|
|Lista Suja (MTE)|CNPJ, CPF, nome, município, CNAE|Empregador responsabilizado por trabalho escravo|Aberto (.txt e .xlsx)|
|CEAC (MTE)|CNPJ, CPF, nome|Empregador com termo de ajustamento de conduta (TAC)|Aberto (.xlsx)|
|CEIS / CNEP (CGU)|CNPJ, CPF|Empresa inidônea, suspensa ou punida|Aberto (API do Portal da Transparência)|
|Novo CAGED (MTE)|Salário de admissão por cargo (CBO) e município|Salário muito acima ou abaixo do padrão local|Aberto (microdados)|
|Tabela CBO (MTE)|Código do cargo|Padroniza o cargo e permite cruzar com o CNAE|Aberto (download)|
|CNAE (IBGE/CONCLA)|Subclasse, divisão e seção da atividade econômica|Permite cruzar a atividade da empresa com o cargo e identificar setores de baixa presença digital|Aberto (download e API do IBGE)|
|Salário mínimo (Banco Central, SGS série 1619) e pisos estaduais|Valor vigente do mínimo nacional, fixado por decreto, e pisos das leis estaduais|Oferta abaixo do mínimo e descontos de moradia e alimentação acima do limite legal|Aberto (API do SGS). Os pisos estaduais vêm das leis de cada estado, numa tabela mantida por nós|
|Mapa de risco (derivado da Lista Suja)|Setor + município de destino|Região e setor com histórico de casos no Cadastro de Empregadores|Gerado por nós|
|IBGE Localidades|Municípios de origem e destino e a região geográfica imediata de cada um|Vaga fora do município ou fora da região imediata|Aberto (API)|
|Registro.br (RDAP)|Data de registro e CNPJ do titular do domínio .br|Site recém-criado ou titular diferente da empresa|Aberto (API)|
|Tabela de DDD (BrasilAPI)|DDD do telefone|DDD sem relação com a empresa ou com a vaga|Aberto (API)|
|Listas de phishing (Phishing.Database, URLhaus)|Links da mensagem|Link malicioso|Aberto (listas públicas)|
|BrasilAPI|Interface única para CNPJ, CEP, DDD e Registro.br|Facilita o acesso às fontes públicas|Aberto (API de código aberto)|

## Fontes públicas fora do MVP

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|SmartLab - Observatório da Erradicação do Trabalho Escravo (MPT/OIT)|Município de origem e de destino, setor econômico|Rota da oferta coincide com um fluxo histórico de aliciamento|Parcial: site aberto, mas sem download documentado. O site usa uma API interna sem documentação pública|
|Radar SIT (MTE)|Resgates por município e por atividade|Região e setor com histórico de resgates|Indisponível: fora do ar, com nova versão em construção, segundo comunicado da SIT|
|GLEIF (LEI)|Registro global de entidades legais|Confirma empresas de médio e grande porte|Aberto (API)|
|Google News (RSS)|Nome da empresa e dos sócios + termos de risco|Menção a resgate ou golpe|Aberto (RSS)|
|Internet Archive|Histórico do site e do LinkedIn|Site ou perfil que surgiu junto com a vaga|Aberto (API)|
|Certificate Transparency (crt.sh)|Histórico de certificados do site|Domínio recém-ativado|Aberto (API)|
|ViaCEP / OpenStreetMap|Endereço da vaga e do CNPJ|Endereço inexistente ou divergente|Aberto (API)|

## Plataformas privadas (fora do MVP)

Sem API pública aberta ou com termos de uso restritivos. Ver o motivo em [escopo-mvp.md](../escopo-mvp.md).

|Fonte|O que consultar|Sinal gerado|Acesso|
|---|---|---|---|
|LinkedIn|Página da empresa, perfil do recrutador|Empresa ou recrutador inexistente, recém-criado ou divergente|Restrito: sem API aberta, só busca na web + Internet Archive|
|Reclame Aqui|Reputação e reclamações|Queixas de golpe ou de vaga falsa|Restrito: sem API pública e com termos de uso restritivos|
|Indeed|Vaga por empresa e data|Mesma vaga publicada pela mesma empresa|Restrito: sem API pública aberta|
|Glassdoor|Avaliações da empresa|Empresa sem histórico ou mal avaliada|Restrito: sem API pública aberta|
|Gupy|Vaga por cargo e empresa|Vaga confirmada no canal oficial|Parcial: API interna sem documentação|
|Catho / Vagas.com / InfoJobs|Vaga por empresa e data|Vaga confirmada ou texto replicado|A verificar|

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
