# Atribuições de dados

O Vaga Segura não redistribui bases de terceiros. O ETL baixa cada base direto da fonte, e o repositório guarda só o código e as tabelas derivadas que nós mesmos calculamos. Mesmo assim, toda tela e todo relatório que usar esses dados deve citar a fonte.

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
| Localidades (municípios, regiões geográficas imediatas e coordenadas) | IBGE | Municípios de origem e destino e relação entre eles | Fonte: IBGE |
| Salário mínimo (SGS, série 1619) | Banco Central do Brasil | Comparação com o salário oferecido e limites de desconto | Fonte: Banco Central do Brasil, SGS |

## Infraestrutura e serviços abertos

| Serviço | Uso no projeto | Condição |
|---|---|---|
| RDAP do Registro.br (NIC.br) | Data de registro e titular de domínios .br | Respeitar os limites de consulta do serviço |
| BrasilAPI | Acesso unificado a CNPJ, CEP, DDD e Registro.br | Código sob licença MIT. Os dados continuam sendo das fontes originais |
| OpenStreetMap / Nominatim | Verificação de endereço | Dados © colaboradores do OpenStreetMap, licença ODbL. A política de uso do Nominatim limita a 1 requisição por segundo |
| ViaCEP | Consulta de CEP | Ver os termos de uso do serviço |
| Listas públicas de phishing (Phishing.Database, URLhaus) | Checagem de links | Ver a licença de cada lista no repositório de origem |
