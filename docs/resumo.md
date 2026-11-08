# Resumo do projeto

O Vaga Segura é uma ferramenta de código aberto que usa inteligência artificial para ajudar trabalhadores brasileiros, principalmente os de baixa renda, a reconhecer sinais de aliciamento para trabalho análogo à escravidão em ofertas de emprego. Essas ofertas circulam por sites, redes sociais e aplicativos de mensagens e costumam prometer salário alto, transporte e alojamento pagos, às vezes com alguma cobrança antecipada e quase nunca com informação sobre o contrato.

Ferramentas parecidas analisam só o texto do anúncio. O Vaga Segura também cruza a oferta com dados públicos brasileiros para ver se ela se sustenta fora da mensagem. A IA roda em modelos de linguagem locais, o que protege a privacidade de quem usa e mantém o custo baixo. Ela tem duas funções: extrair do texto o que pode ser verificado (empresa, CNPJ, cargo, local, salário e promessas) e, no fim, explicar o resultado em linguagem simples. As verificações e a pontuação ficam com regras fixas, para que cada ponto possa ser auditado.

A verificação acontece em etapas. Primeiro, confirmamos se a empresa existe e está ativa na Receita Federal. Depois, verificamos se ela ou seus sócios aparecem no Cadastro de Empregadores do Ministério do Trabalho e Emprego (a "Lista Suja") ou nos cadastros de sanções da CGU. O salário prometido é comparado com o que o Novo CAGED registra para o mesmo cargo na região, e o deslocamento proposto também entra na conta: levar o trabalhador para longe com transporte e alojamento pagos é um padrão conhecido de aliciamento. Plataformas privadas, como Reclame Aqui, LinkedIn e sites de vagas, ficam para uma etapa posterior. Cada verificação gera evidências com peso próprio, e o conjunto vira uma pontuação de confiança na vaga.

Quem usa recebe essa pontuação junto com as evidências explicadas em linguagem simples, orientações de prevenção e, quando for o caso, os canais oficiais de denúncia, como o Sistema Ipê e o MPT Pardal. O resultado serve para a pessoa decidir se aceita a proposta; apurar o caso continua sendo papel da fiscalização. O projeto responde ao tema da edição 2027 do AI4Good, "O Brasil em primeira pessoa": usa só dados públicos brasileiros e parte de um padrão de aliciamento comum no país. O projeto se alinha à ODS 8, meta 8.7, que trata da erradicação do trabalho forçado e da escravidão moderna.

## Referências

- [MTE - Combate ao trabalho escravo e Cadastro de Empregadores](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo)
- [Sistema Ipê - denúncias de trabalho análogo à escravidão](https://ipe.sit.trabalho.gov.br/)
- [MPT Pardal - orientações de uso](https://www.prt17.mpt.mp.br/informe-se/noticias-do-mpt-es/962-pgt-traz-orientacoes-de-uso-do-aplicativo-mpt-pardal)
- [ONU Brasil - ODS 8: Trabalho decente e crescimento econômico](https://brasil.un.org/pt-br/sdgs/8)
