# Atribuições de dados

O Vaga Segura não redistribui bases de terceiros. O ETL baixa cada base direto da fonte e grava no banco local as tabelas, inclusive as derivadas que nós calculamos. O repositório guarda só o código. Mesmo assim, toda tela e todo relatório que usar esses dados deve citar a fonte.

## Dados públicos oficiais

Publicados por órgãos do governo federal em transparência ativa (Lei 12.527/2011). Uso livre, com citação da fonte.

| Base | Responsável | Uso no projeto | Como citar |
|---|---|---|---|
| Cadastro Nacional da Pessoa Jurídica (CNPJ e QSA) | Receita Federal | Situação, abertura, CNAE, porte e sócios da empresa | Fonte: Receita Federal do Brasil |
| Cadastro de Empregadores (Lista Suja) | Ministério do Trabalho e Emprego | Cruzamento de empregadores e sócios | Fonte: MTE, Cadastro de Empregadores (Portaria Interministerial MTE/MDHC/MIR nº 18/2024) |
| Cadastro de Empregadores em Ajustamento de Conduta (CEAC) | Ministério do Trabalho e Emprego | Cruzamento de empregadores | Fonte: MTE, CEAC |
| CEIS e CNEP | Controladoria-Geral da União | Sanções vigentes | Fonte: CGU, Portal da Transparência. A API exige chave de acesso gratuita |
| Novo CAGED (microdados) | Ministério do Trabalho e Emprego (PDET) | Salário de admissão por cargo e região, compatibilidade entre CNAE e cargo | Fonte: MTE, Novo CAGED |
| Classificação Brasileira de Ocupações (CBO) | Ministério do Trabalho e Emprego | Padronização de cargos | Fonte: MTE, CBO |
| Classificação Nacional de Atividades Econômicas (CNAE 2.3, subclasses) | IBGE (CONCLA) | Atividade da empresa, compatibilidade com o cargo e setores de baixa presença digital | Fonte: IBGE, CONCLA |
| Localidades (municípios, regiões geográficas imediatas e coordenadas) | IBGE | Municípios de origem e destino e relação entre eles | Fonte: IBGE |
| Salário mínimo (SGS, série 1619) | Banco Central do Brasil | Comparação com o salário oferecido e limites de desconto | Fonte: Banco Central do Brasil, SGS |
| Pisos salariais estaduais | Assembleias legislativas dos estados | Comparação com o salário oferecido, quando o piso do estado é maior que o mínimo | Fonte: lei estadual de cada piso, citada na tabela |

## Infraestrutura e serviços abertos

| Serviço | Uso no projeto | Condição |
|---|---|---|
| RDAP do Registro.br (NIC.br) | Data de registro e titular de domínios .br | Respeitar os limites de consulta do serviço |
| BrasilAPI | Acesso unificado a CNPJ, CEP, DDD e Registro.br | Código sob licença MIT. Os dados continuam sendo das fontes originais |
| OpenStreetMap / Nominatim | Verificação de endereço (fora do MVP) | Dados © colaboradores do OpenStreetMap, licença ODbL. A política de uso do Nominatim limita a 1 requisição por segundo |
| ViaCEP | Consulta de CEP (fora do MVP) | Ver os termos de uso do serviço |
| Listas públicas de phishing (Phishing.Database, URLhaus) | Checagem de links | Ver a licença de cada lista no repositório de origem |
| Google Safe Browsing (Update API) | Checagem de links da camada geral, por hash | Gratuito só para uso não comercial (uso comercial exige o Web Risk). Os avisos baseados nessa lista citam o Google como fonte e dizem que a proteção não é perfeita, como pedem os termos do serviço |
| Consumidor.gov.br (Senacon) | Reclamações por empresa (fora do MVP, fase 2) | Dados abertos do Ministério da Justiça, com citação da fonte |
