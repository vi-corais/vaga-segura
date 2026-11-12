# Contratos entre os módulos

Cada etapa do motor conversa com a seguinte por um formato fixo, definido em Pydantic. Assim cada pessoa da equipe consegue trabalhar no seu módulo sem depender do código das outras, e qualquer mudança de formato aparece na revisão.

![Arquitetura](arquitetura.excalidraw.png)

## Fluxo

```
EntradaAnalise                   -> [1. Extração]      -> ExtracaoOferta
EntradaAnalise + ExtracaoOferta  -> [2. Normalização]  -> Normalizacao
ExtracaoOferta + Normalizacao    -> [3. Coletores]     -> ResultadoColetor (x9)
ResultadoColetor (x9) + catálogo -> [4. Pontuação]     -> Pontuacao
Pontuacao + verificações         -> [5. Classificação] -> Classificacao
tudo acima                       -> [6. Explicação]    -> ResultadoAnalise
```

| Etapa | Recebe | Devolve | Onde está o formato |
|---|---|---|---|
| Entrada (API e webhook do WhatsApp) | Texto da oferta ou do print, canal de origem e o município do perfil do usuário | `EntradaAnalise` | `app/modelos/extracao.py` |
| 1. Extração (IA local) | `EntradaAnalise` | `ExtracaoOferta` | `app/modelos/extracao.py` e `schemas/extracao.schema.json` |
| 2. Normalização (regras) | `EntradaAnalise` + `ExtracaoOferta` | `Normalizacao` | `app/modelos/extracao.py` |
| 3. Coletores | `ExtracaoOferta` + `Normalizacao` | `ResultadoColetor` | `app/modelos/evidencia.py` |
| 4. Pontuação | Todos os `ResultadoColetor` + catálogo | `Pontuacao` | `app/modelos/evidencia.py`, `app/modelos/catalogo.py` e `catalogo/evidencias.yaml` |
| 5. Classificação | `Pontuacao` + verificações | `Classificacao` | `app/modelos/evidencia.py` e `catalogo/evidencias.yaml` (faixas) |
| 6. Explicação | Evidências, pontuação e classificação | `ResultadoAnalise` | `app/modelos/evidencia.py` |

Tipos usados por mais de um módulo (canal, origem, relação de localidade, coletores e faixas) ficam em `app/modelos/base.py`.

## Contrato 1: extração e normalização

`ExtracaoOferta` é o que a IA devolve. O mesmo modelo gera o `schemas/extracao.schema.json`, que vai para o Ollama como formato obrigatório da resposta, então a IA não consegue devolver um JSON fora do padrão.

Todo valor informado carrega o trecho literal do texto que o justifica (`Campo.trecho`, ou o campo `trecho` do próprio objeto). O esquema recusa valor informado sem trecho; campos com `nao_informado` não precisam de trecho. Antes de seguir, conferimos se o trecho existe mesmo no texto original, e o campo cujo trecho não aparece é descartado.

Campos extraídos: empresa (nome e CNPJ), recrutador, cargo, quantidade de vagas, salário (valor e período), local de trabalho (com a modalidade: presencial, remoto ou híbrido), benefícios (incluindo adiantamento), cobranças, descontos no salário, forma e momento do pagamento, contrato, contatos (telefones, e-mails, links, chaves PIX) e sinais de texto (urgência, dispensa de requisitos, pedido de documentos originais, compra em estabelecimento indicado, entre outros).

`Normalizacao` é feita só com regras, sem IA, a partir da `ExtracaoOferta` e da `EntradaAnalise` (de onde vem o município de origem): CNPJ com dígitos validados, nome da empresa normalizado, código CBO do cargo, municípios de origem e destino no código do IBGE, a relação entre eles (ver a próxima seção), salário mensal estimado, salário mínimo de referência, domínios e DDDs.

## Perfil e localidade

O município de origem vem do perfil: a pessoa informa uma vez onde mora. No WhatsApp, o bot pergunta na primeira conversa e guarda só o município, ligado a um HMAC do número (tabela `perfis_usuario`). No site, o perfil fica no próprio navegador. Escolaridade e outros dados pessoais não são pedidos, porque nenhuma regra do catálogo usa essas informações (LGPD, art. 6º, III).

Com o município da pessoa e o da vaga, a normalização preenche `relacao_localidade`:

| Valor | Quando | Efeito |
|---|---|---|
| `mesmo_municipio` | A vaga é no município onde a pessoa mora | Evidências de deslocamento não se aplicam |
| `mesma_regiao_imediata` | Outro município da mesma região geográfica imediata | Vale o art. 207 do CP (outra localidade), com peso menor |
| `outra_regiao_imediata` | Fora da região imediata, em outra UF ou no exterior | Vale o art. 207, com peso maior |
| `nao_se_aplica` | Trabalho remoto | Evidências de deslocamento ficam como `nao_aplicavel` |
| `desconhecida` | Sem perfil ou sem local da vaga | Evidências de deslocamento ficam como `sem_dados` |

A região geográfica imediata é a divisão do IBGE que agrupa municípios em torno de um centro urbano, pelo deslocamento diário para trabalho, comércio e serviços. Usamos essa divisão, e não uma distância fixa em km, porque nenhuma norma define uma distância. O art. 207 fala só em "outra localidade", então qualquer vaga fora do município já conta. A distância em km é calculada só para exibir ao usuário. A diferença de peso entre os dois casos é um parâmetro inicial, a calibrar com o conjunto de teste.

## Contrato 2: evidências

Todo coletor segue a mesma assinatura:

```python
async def coletar(extracao: ExtracaoOferta, norm: Normalizacao) -> ResultadoColetor
```

`ResultadoColetor` tem duas listas:

- `verificacoes`: cada checagem tentada, identificada pelo coletor e pelo nome da checagem (ex.: `cnpj` + `cnpj_situacao`), com status `concluida`, `nao_aplicavel`, `falhou` ou `sem_dados`. É daqui que sai a cobertura da análise.
- `evidencias`: os fatos encontrados (`EvidenciaColetada`), cada um com o id do catálogo, a fonte, a data da fonte, o trecho da oferta, o valor observado e a referência de comparação. Não há campo de pontos: o coletor não sabe quanto a evidência vale.

Regras:

- Fonte que falha vira `falhou`, nunca evidência de risco.
- O coletor não decide pontos. Na etapa 4, o motor transforma cada `EvidenciaColetada` em `Evidencia`, com direção, força, pontos e base legal do catálogo, e calcula `pontos_aplicados`.
- `confianca_coleta` (de 0 a 1) indica a qualidade do dado. Um cruzamento aproximado, por exemplo, entra com valor menor que 1.

Os 8 coletores:

| Coletor | No diagrama | O que verifica | Dados |
|---|---|---|---|
| `cnpj` | Receita CNPJ / QSA | Existência, situação, idade, porte e endereço da empresa; se o empregador é identificável | BrasilAPI (Receita Federal) |
| `listas_mte` | Lista Suja / CEAC | Empresa, empregador e sócios nos cadastros do MTE | `empregadores_mte` |
| `sancoes` | CEIS / CNEP | Sanções vigentes da CGU | `sancoes` |
| `salario` | Salário (CAGED e mínimo) | Salário comparado ao CAGED e ao mínimo; limites de desconto | `salarios_cbo`, `salario_minimo_pisos` |
| `coerencia` | CNAE x CBO | Atividade e porte da empresa comparados ao cargo e às vagas | `cnae_cbo_compatibilidade` |
| `rota` | Localidade (IBGE) | Deslocamento com transporte ou alojamento, passagem descontada, destino com histórico de casos | `municipios`, `mapa_risco` |
| `contato` | Contatos e domínio | Links, domínio, e-mail e DDD | RDAP, listas de phishing, BrasilAPI (DDD) |
| `texto` | Texto da oferta | Cobranças, descontos, forma e momento do pagamento, sinais de texto | `ExtracaoOferta` |

## Contrato 3: catálogo

`catalogo/evidencias.yaml` é a única fonte de pesos, tetos e base legal. O código do motor só lê esse arquivo. O validador em `app/modelos/catalogo.py` recusa o catálogo se:

- uma evidência de risco tiver pontos positivos (ou o contrário);
- houver id repetido;
- um teto, uma evidência (`aplica_quando`) ou um indicador de combinação usar uma condição que não foi definida;
- uma combinação apontar para uma evidência que não existe, ou para um caminho da extração que não existe (ex.: `beneficios.alojamento`);
- uma evidência usar um coletor fora da lista acima ou um critério de cruzamento desconhecido;
- uma evidência de confiança tiver teto;
- as faixas estiverem fora de ordem, ou os bônus de uma combinação não forem crescentes.

Para conferir: `python scripts/validar_catalogo.py`.

Na etapa 4, o motor faz a soma ponderada das evidências e aplica o bônus de combinação (indicadores do PL 1636, art. 2º, IV), o ajuste de ausência por setor e os tetos. Dos bônus de uma combinação, vale só o maior atingido. O indicador `publico_migrante` só conta dentro da combinação: sozinho, não pontua, para não penalizar vagas legítimas voltadas a migrantes.

Na etapa 5, o motor calcula a cobertura (verificações concluídas sobre verificações aplicáveis) e define a faixa:

| Pontuação | Faixa |
|---|---|
| 0 a 34 | `alto_risco` |
| 35 a 64 | `atencao` |
| 65 a 100 | `sem_sinais_relevantes` |

Se a cobertura ficar abaixo de 40% e a pontuação passar de 64, a faixa vira `inconclusivo`: foram feitas poucas verificações para afirmar que não há sinais. Com pontuação até 64, a faixa de risco encontrada é mantida. Os limites ficam em `faixas`, no catálogo.

## Resultado final

`ResultadoAnalise` traz a pontuação (0 a 100), a faixa (`alto_risco`, `atencao`, `sem_sinais_relevantes` ou `inconclusivo`), a cobertura, os tetos aplicados, as evidências, as verificações e a explicação. Também registra o modelo de IA usado, a origem (texto ou imagem), o canal e a relação de localidade. Cada item da explicação aponta para o id de uma evidência, e o próprio modelo `ResultadoAnalise` recusa qualquer item que não tenha uma evidência correspondente (guardrail).

## Versões

Cada análise registra `versao_esquema` (formato da extração) e `versao_catalogo` (pesos usados). Mudou um campo ou um peso, sobe a versão. Isso permite comparar análises antigas e novas na calibração.
