# Escopo do MVP

## Entra no MVP

|Item|O que inclui|
|---|---|
|Entrada|Texto e print da oferta (com OCR), pelo WhatsApp ou pelo site|
|Canal WhatsApp|Bot pela API oficial do WhatsApp (Cloud API, da Meta): recebe a oferta encaminhada e responde com o resultado. Respostas a mensagens enviadas pelo usuário são gratuitas|
|Perfil|Município onde a pessoa mora, informado uma vez. No WhatsApp, fica guardado ligado a um HMAC do número; no site, fica no navegador|
|Extração|Modelo de linguagem local (Ollama) com saída obrigatória em JSON Schema, cada campo com o trecho de origem|
|Normalização|Validação de CNPJ, cargo convertido em CBO, municípios no código do IBGE, relação entre o município da pessoa e o da vaga (região imediata do IBGE) e salário mensal|
|Bases locais|ETL da Lista Suja, CEAC, CEIS/CNEP, Novo CAGED agregado, CBO, IBGE (municípios e regiões imediatas) e salário mínimo (Banco Central)|
|Coletores|Os 9 descritos em [contratos.md](arquitetura/contratos.md): CNPJ + QSA, listas MTE, sanções, salário, coerência, rota, contato, texto e base própria|
|Base própria|Só o registro de textos e contatos (telefones, e-mails e chaves PIX) repetidos, sem relatos|
|Motor de cálculo|Catálogo YAML, agregador, combinação, ajuste de ausência por setor, tetos, cobertura e faixa|
|Explicação|Texto em linguagem simples gerado só a partir das evidências, com guardrail|
|Interface|PWA leve (FastAPI + HTMX), pensada para celular simples|
|Calibração|Conjunto de teste com casos de risco e legítimos, e as métricas de precisão e falsos positivos|
|Infraestrutura|Docker Compose com API, Ollama e PostgreSQL, com endereço HTTPS público para o webhook do WhatsApp|

## Não entra no MVP

|Item|Motivo|
|---|---|
|Áudio (transcrição)|Depende de outro modelo e aumenta o tempo de resposta. No MVP, o bot pede que a oferta seja enviada em texto ou print|
|LinkedIn, Indeed, Gupy e Reclame Aqui|Sem API pública aberta e com termos de uso restritivos|
|SmartLab (rotas de aliciamento)|Não tem download documentado. A integração depende de acesso estável aos dados de origem e destino|
|Relatos colaborativos|É a parte com mais risco jurídico (dano à imagem, difamação) e precisa de moderação|
|Painel institucional|Só faz sentido com volume de uso e parceiros definidos|
|Calibração estatística (log-odds)|Precisa de dados de uso real para ajustar os pesos|
