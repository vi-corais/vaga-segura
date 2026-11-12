# Pradhan e Shehory (2026): tráfico laboral online e machine learning

## Sobre o estudo

Revisão de escopo de 21 estudos publicados entre janeiro de 2002 e setembro de 2025. Desses, 14 tratam de tráfico laboral e 7 de tráfico sexual, incluídos porque os métodos podem ser aproveitados. Deixamos de lado a parte sobre treinamento de modelos (desbalanceamento de classes, SMOTE, active learning), que não se aplica ao nosso caso.

A revisão trata de tráfico laboral, então embasa sobretudo a camada de gravidade do Vaga Segura. Os achados sobre sinais fracos, pontos cegos digitais e falsos positivos valem também para a camada geral (golpes de falso emprego), cujos sinais vêm de alertas da Febraban, de guias de segurança e das ferramentas analisadas em `interno/projetos-semelhantes.md`.

## Dificuldades que cruzam com o Vaga Segura

### 1. O sinal no anúncio é fraco por natureza
*Discussion -> Structural constraints*

Coerção, servidão por dívida e retenção de documentos acontecem dentro da relação de trabalho, depois do recrutamento, então não aparecem nos dados da fase de recrutamento. Como o engano depende de o anúncio parecer lícito, o sinal é fraco. Para os autores, os sinais mais fortes são as irregularidades econômicas que aparecem dentro de documentos lícitos.

Foi por isso que decidimos validar a oferta fora do texto. Mas uma empresa real, ativa e com CNPJ regular ainda pode aliciar, e a verificação não pega esse caso.

### 2. A exploração só aparece onde há rastro digital
*Discussion -> Socio-technical implications*

O artigo observa que setores como construção e trabalho doméstico tendem a ficar sub-representados, e que a IA pode reforçar pontos cegos que a pesquisa e a fiscalização já têm.

É o ponto que mais afeta o projeto. O público de baixa renda costuma receber ofertas rurais, de construção, de trabalho doméstico e de colheita, e esses empregadores raramente têm LinkedIn, perfil no Reclame Aqui ou vaga no Indeed. Se a ausência nessas fontes derrubasse a pontuação, o sistema marcaria como suspeitas justamente as vagas legítimas desse público. Uma observação nossa, que não vem do artigo: no aliciamento para trabalho escravo no Brasil, quem recruta muitas vezes é um intermediário (o "gato"), e não a empresa que aparece no anúncio.

### 3. Fontes diferentes medem coisas diferentes
*Discussion -> Methodological implications*

Como cada registro é criado com um propósito, cada conjunto de dados capta um construto diferente, e não outra observação do mesmo fenômeno.

Vale para a nossa pontuação: CNPJ ativo, Lista Suja, reputação no Reclame Aqui e presença no LinkedIn medem coisas diferentes. Por isso cada fonte tem um papel no catálogo, umas confirmando legitimidade e outras indicando risco.

### 4. Indicadores fortes e fracos, nunca binários
*Discussion -> Way forward*

A recomendação é tratar os indicadores como uma combinação de sinais fracos e fortes, ponderados pela força preditiva. Eles costumam aparecer juntos e dependem de contexto.

O catálogo de evidências segue essa ideia: constar na Lista Suja é um indicador forte, e não ter LinkedIn é fraco.

### 5. Falta de gabarito para validar
*Discussion -> Methodological implications e Way forward*

Os autores apontam a falta de validação contra casos confirmados como a lacuna que mais se repete nos estudos da fase de recrutamento. Na prática, a acurácia publicada mede a concordância com um indicador indireto, e não a detecção do tráfico.

Mesmo sem treinar modelo, precisamos calibrar os pesos e mostrar que a pontuação funciona. O plano é testar com casos documentados de resgate, com golpes de falso emprego já noticiados e com vagas reais conhecidas, e publicar as métricas separadas por camada. As fontes escolhidas e o formato dos casos estão em [`calibracao/`](../../calibracao/README.md).

### 6. Falsos positivos estigmatizam
*Discussion -> Socio-technical implications*

Segundo os autores, falsos positivos podem estigmatizar empresas ou trabalhadores legítimos, enquanto falsos negativos deixam a exploração sem resposta. É o mesmo risco de dano à imagem que aparece na parte jurídica.

### 7. Apoio à decisão e explicabilidade
*Way forward*

Os autores recomendam ferramentas de apoio à decisão humana, e não de detecção autônoma. Modelos baseados em pontuação ganham em transparência, ainda que percam um pouco de acurácia. Como a nossa pontuação é feita de evidências verificáveis, dá para explicar cada ponto dela.

### 8. Fontes externas somem ou mudam
*Limitations*

Um dos conjuntos de dados citados ficou inacessível depois que a plataforma de origem mudou de domínio por pressão policial. A revisão não discute termos de uso, políticas de API nem limites de requisição.

Depender de Reclame Aqui, LinkedIn e Indeed é um risco técnico e jurídico que a literatura não resolve. Foi um dos motivos para deixar essas fontes fora do MVP.

### 9. Poucos indicadores são observáveis online
*Introduction e Discussion*

Só 10 dos 59 indicadores do UNODC puderam ser operacionalizados online. Por isso o Vaga Segura se apresenta como uma triagem preventiva. Detectar trabalho escravo a partir de um anúncio está fora do alcance de qualquer ferramenta desse tipo.

## Estudos citados na revisão que podem ser úteis

- [Volodko et al. (2020)](https://doi.org/10.1007/s12117-019-09376-5) operacionalizaram indicadores para anúncios voltados a migrantes: violações de salário e jornada, descrição vaga da função, redirecionamento para fora da plataforma e benefícios como alojamento, transporte, ida para o país de destino e ajuda para se instalar. A lista é muito parecida com a nossa e pode ser citada como base.
- [Da Silva Santos et al. (2019)](https://doi.org/10.1109/ICMLA.2019.00132) identificam risco de escravidão moderna em municípios brasileiros a partir de dados socioeconômicos, demográficos e de operações de resgate. Pode servir de camada de contexto regional, por exemplo para uma oferta que leva o trabalhador a um município de alto risco.

## Referências

- [Pradhan, R.; Shehory, O. (2026). Online labor trafficking and machine learning: A scoping review and research agenda. PLOS ONE](https://doi.org/10.1371/journal.pone.0358425)
- [Texto completo no PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC13606961/)
- [Volodko, A.; Cockbain, E.; Kleinberg, B. (2020). "Spotting the signs" of trafficking recruitment online: exploring the characteristics of advertisements targeted at migrant job-seekers. Trends in Organized Crime, 23, 7-35](https://doi.org/10.1007/s12117-019-09376-5)
- [Da Silva Santos, M.; Ladeira, M.; Van Erven, G. C. G.; Silva, G. L. (2019). Machine Learning Models to Identify the Risk of Modern Slavery in Brazilian Cities. 18th IEEE International Conference on Machine Learning and Applications (ICMLA), 740-746](https://doi.org/10.1109/ICMLA.2019.00132)
