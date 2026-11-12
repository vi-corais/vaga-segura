# Escopo do MVP

O MVP cobre as duas camadas da análise. A camada geral (golpes de falso emprego em qualquer vaga) reaproveita os coletores que já existem e acrescenta regras de texto e de contato. A camada de gravidade (aliciamento para trabalho análogo à escravidão) é o diferencial do projeto e continua inteira no MVP.

## Ordem de entrega

O MVP é entregue em dois níveis, para que o Demo Day tenha um caminho completo funcionando mesmo que o tempo aperte. Como os contratos entre os módulos já estão fixos e testados, o que fica para o segundo nível entra depois sem mudar o que já foi feito.

|Nível|O que inclui|
|---|---|
|1. Núcleo garantido|Entrada por texto (site e WhatsApp, com o número de teste da Cloud API), extração no Ollama com validação dos trechos, normalização de CNPJ, municípios e região imediata, e os coletores `cnpj`, `listas_mte`, `texto` e `rota`. Entram todas as evidências desses quatro coletores, menos `destino_setor_alto_risco`, que depende do mapa de risco. Motor de pontuação lendo o catálogo, faixa, cobertura, alerta de aliciamento e explicação montada a partir das evidências|
|2. Se der tempo, nesta ordem|OCR de print, coletor `salario` (ETL do Novo CAGED, o mais pesado), coletor `contato` (RDAP, listas de phishing e links encurtados), `sancoes`, `coerencia`, mapa de risco, PWA completa e explicação reescrita pelo modelo com guardrail|

Sem o coletor `salario`, a combinação de indícios do PL 1636 funciona só com os indicadores que vêm do texto (alojamento, pagamento em espécie e público migrante). As verificações que não rodarem aparecem como `nao_aplicavel` e baixam a cobertura, como prevê o contrato.

Infraestrutura da demo: o modelo roda na máquina da equipe e o webhook do WhatsApp chega por um túnel HTTPS (Cloudflare Tunnel). Para ficar no ar depois do programa, é preciso um servidor com GPU ou uma VPS com um modelo menor.

## Entra no MVP

|Item|O que inclui|
|---|---|
|Entrada|Texto e print da oferta (com OCR), pelo WhatsApp ou pelo site|
|Canal WhatsApp|Bot pela API oficial do WhatsApp (Cloud API, da Meta): recebe a oferta encaminhada e responde com o resultado. Respostas a mensagens enviadas pelo usuário são gratuitas|
|Perfil|Município onde a pessoa mora, informado uma vez. No WhatsApp, fica guardado ligado a um HMAC do número; no site, fica no navegador|
|Extração|Modelo de linguagem local (Ollama) com saída obrigatória em JSON Schema, cada campo com o trecho de origem. Inclui os sinais de golpe (tarefa paga, pedido de código ou senha, dados sensíveis, conta laranja, instalar app) e a finalidade de cada chave PIX|
|Normalização|Validação de CNPJ, cargo convertido em CBO, municípios no código do IBGE, relação entre o município da pessoa e o da vaga (região imediata do IBGE), salário mensal, domínios, e-mail pessoal e links encurtados|
|Bases locais|ETL da Lista Suja, CEAC, CEIS/CNEP, Novo CAGED agregado, CBO, IBGE (municípios e regiões imediatas) e salário mínimo (Banco Central)|
|Coletores|Os 8 descritos em [contratos.md](arquitetura/contratos.md): CNPJ + QSA, listas MTE, sanções, salário, coerência, rota, contato e texto|
|Links|Listas públicas de phishing (Phishing.Database, URLhaus) e Google Safe Browsing (Update API, por hash). Links encurtados têm o destino descoberto no servidor, sem abrir a página|
|Motor de cálculo|Catálogo YAML com as duas camadas, agregador, combinação, ajuste de ausência por setor, tetos, cobertura, faixa, alerta de aliciamento e categorias do problema encontrado|
|Explicação|Texto em linguagem simples gerado só a partir das evidências, com guardrail. Traz perguntas para fazer ao recrutador, a ação urgente na primeira linha quando houver link, app ou pedido de código ("não clique", "não instale", "não passe o código") e os canais de acordo com o tipo de problema|
|Interface|PWA leve (FastAPI + HTMX), pensada para celular simples|
|Calibração|Conjunto de teste com casos de risco das duas camadas e casos legítimos, e as métricas de precisão e falsos positivos|
|Infraestrutura|Docker Compose com API, Ollama e PostgreSQL, com endereço HTTPS público para o webhook do WhatsApp|

## O que cada camada verifica no MVP

|Camada|Verificações|
|---|---|
|Geral|Empresa na Receita (existe, ativa, idade, porte, CNAE x cargo), sanções da CGU, domínio e titular no Registro.br, links maliciosos e encurtados, e-mail gratuito, DDD, chave PIX de terceiro, cobranças antecipadas, golpe da tarefa, pedido de código, senha ou dados sensíveis, conta laranja, instalar app, urgência, ganho garantido|
|Gravidade|Lista Suja e CEAC (empresa, empregador e sócios), transporte e alojamento para outra localidade (art. 207), passagem descontada, mapa de risco por destino e setor, adiantamento, pagamento só no fim do serviço, descontos acima do limite legal, compra em estabelecimento indicado e a combinação de indícios do PL 1636|
|Ambas|Cobrança antecipada, salário fora do padrão do CAGED ou abaixo do mínimo, pedido de documentos originais, pagamento só em dinheiro vivo e pedido de sigilo|

Os canais de denúncia acompanham o tipo de problema: banco e MED do PIX, boletim de ocorrência e a plataforma onde a vaga apareceu para golpes; Sistema Ipê, MPT Pardal e Disque 100 quando o alerta de aliciamento liga.

## Não entra no MVP

|Item|Motivo|
|---|---|
|Áudio (transcrição)|Depende de outro modelo e aumenta o tempo de resposta. No MVP, o bot pede que a oferta seja enviada em texto ou print|
|Extensão de navegador|Fica para a fase 2 do [roteiro](roteiro.md). É o formato padrão desse tipo de ferramenta, mas o público principal recebe as ofertas pelo WhatsApp, que já é coberto no MVP|
|LinkedIn, Indeed, Gupy e Reclame Aqui|Sem API pública aberta e com termos de uso restritivos. Para golpes em geral, Reclame Aqui e LinkedIn teriam peso maior, mas o problema dos termos de uso continua|
|SmartLab (rotas de aliciamento)|Camada de gravidade. Não tem download documentado. A integração depende de acesso estável aos dados de origem e destino|
|Base própria (textos e contatos repetidos)|Guardar telefones, e-mails e chaves PIX que aparecem nas ofertas, mesmo em hash, exige cuidados de segurança e de LGPD que não cabem no MVP, e o sinal só tem valor com volume de uso. Entra depois, se o app crescer, como retroalimentação das próprias análises|
|Lista de marcas imitadas e domínios parecidos|Mesmo caso da base própria. Detectar quem se passa por uma marca conhecida (Magazine Luiza, Localiza, BNE etc.) exige uma lista curada de marcas, CNPJs e domínios oficiais, mantida com revisão humana e regras claras para não acusar revendedoras e terceirizadas. Depende do crescimento da aplicação e de uma equipe de revisão|
|Relatos colaborativos|É a parte com mais risco jurídico (dano à imagem, difamação) e precisa de moderação|
|Painel institucional|Só faz sentido com volume de uso e parceiros definidos|
|Calibração estatística (log-odds)|Precisa de dados de uso real para ajustar os pesos|
