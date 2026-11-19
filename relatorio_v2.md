# Relatório de pedidos (orquestrador v2)

Gerado em 19/11/2026.

A validação (seção 1) analisa a base original, ainda suja. A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.

## 1. Validação dos dados

1. Gravidade: Alta
- Problema: Preço unitário negativo
- Quantidade: 21 linhas
- Ação: Separar as linhas para revisão

2. Gravidade: Alta
- Problema: Quantidade zero ou negativa
- Quantidade: 45 linhas
- Ação: Separar as linhas para revisão

3. Gravidade: Alta
- Problema: Preço unitário nulo
- Quantidade: 71 linhas
- Ação: Separar as linhas para revisão

4. Gravidade: Média
- Problema: Linhas duplicadas
- Quantidade: 118 linhas
- Ação: Remover as linhas duplicadas

5. Gravidade: Média
- Problema: Frete como texto (valores com "R$" e vírgula)
- Quantidade: 5118 linhas
- Ação: Converter os valores de frete para o formato numérico

6. Gravidade: Média
- Problema: Datas em formato misto (DD/MM/AAAA misturado com AAAA-MM-DD)
- Quantidade: 1292 datas em formato BR
- Ação: Padronizar todas as datas para o formato AAAA-MM-DD

7. Gravidade: Baixa
- Problema: Estado nulo
- Quantidade: 163 linhas
- Ação: Recuperar os valores a partir de outras colunas da própria base

8. Gravidade: Baixa
- Problema: Categoria nula
- Quantidade: 56 linhas
- Ação: Recuperar os valores a partir de outras colunas da própria base

9. Gravidade: Baixa
- Problema: Variações no texto da cidade
- Quantidade: 52 valores distintos, 12 após padronizar
- Ação: Padronizar os textos ignorando maiúsculas, acentos e espaços

10. Gravidade: Baixa
- Problema: Variações no texto da categoria
- Quantidade: 15 valores distintos, 5 após padronizar
- Ação: Padronizar os textos ignorando maiúsculas, acentos e espaços

11. Gravidade: Baixa
- Problema: Variações no texto do status
- Quantidade: 12 valores distintos, 4 após padronizar
- Ação: Padronizar os textos ignorando maiúsculas, acentos e espaços

12. Gravidade: Baixa
- Problema: Cidade nula
- Quantidade: 31 linhas
- Ação: Recuperar os valores a partir do estado quando o estado tiver uma única cidade na base ou separar as linhas para revisão caso contrário

Total de problemas listados: 12

A base não está pronta para análise.

## 2. Análise comercial

1. Visão geral: total de pedidos, unidades, receita total e crescimento de 2024 sobre 2023.
A loja registrou um total de 4.871 pedidos, com 9.665 unidades vendidas e uma receita total de R$ 2.081.332,37. O crescimento das unidades vendidas em 2024 em comparação a 2023 foi de 35,04%.

2. Categorias: unidades e receita de cada categoria, e quais mudam de posição entre unidades e receita.
Na categoria Eletrônicos foram vendidas 2.527 unidades com receita de R$ 821.515,52. Em Moda foram 2.333 unidades e receita de R$ 416.218,29, em Casa & Decoracao foram 1.907 unidades e receita de R$ 326.748,39, em Beleza foram 1.560 unidades e receita de R$ 385.033,1, e em Esporte foram 1.338 unidades e receita de R$ 131.817,07. As categorias Beleza e Casa & Decoracao mudam de posição entre unidades e receita.

3. Ticket médio: o ticket médio de cada uma das 5 categorias.
O ticket médio de Eletrônicos é de R$ 325,1, de Moda é de R$ 178,4, de Beleza é de R$ 246,82, de Casa & Decoracao é de R$ 171,34 e de Esporte é de R$ 98,52.

4. Estados: os 3 primeiros e o último colocado em unidades, e se o ticket médio é parecido entre os estados.
O primeiro colocado em unidades é SP com 3.405 unidades, o segundo é RJ com 1.150 unidades, o terceiro é MG com 995 unidades, e o último colocado é GO com 341 unidades. O ticket médio é parecido entre os estados, variando entre R$ 199,73 e R$ 221,51.

5. Canais: unidades, receita e ticket médio dos 3 canais, destacando o maior ticket médio.
No canal site foram vendidas 4.384 unidades com receita de R$ 947.832,27 e ticket médio de R$ 216,2. No app foram 3.401 unidades, receita de R$ 715.029,05 e ticket médio de R$ 210,24, enquanto no marketplace foram 1.880 unidades, receita de R$ 418.471,05 e ticket médio de R$ 222,59, sendo este último o canal com o maior ticket médio.

6. Cancelamento: a taxa geral e a taxa de cada uma das 5 categorias.
A taxa de cancelamento geral da loja foi de 7,92%. Por categoria, a taxa de cancelamento foi de 8,45% em Eletrônicos, 7,95% em Moda, 7,88% em Beleza, 6,7% em Casa & Decoracao e 8,66% em Esporte.

7. Sazonalidade: os 3 meses mais fortes e os 3 mais fracos.
Os 3 meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades. Os 3 meses mais fracos em unidades vendidas foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: Os dados cobrem apenas o período de janeiro de 2023 a dezembro de 2024 e não incluem informações sobre custos operacionais ou margem de lucro dos produtos.

## 3. Recomendações

1. Separe as 21 linhas com preço unitário negativo, as 45 linhas com quantidade zero ou negativa e as 71 linhas com preço unitário nulo para revisão, conforme apontado na validação dos dados.
Classificação: Os dados provam

2. Invista e mantenha os recursos na categoria Eletrônicos, que lidera com 2.527 unidades e receita de R$ 821.515,52.
Classificação: Os dados provam

3. Investigue o motivo do baixo volume de vendas da categoria Esporte, que registrou 1.338 unidades e receita de R$ 131.817,07, sendo a categoria mais fraca.
Classificação: Os dados só sugerem

4. Invista em campanhas e ações comerciais para o canal marketplace, que possui o maior ticket médio de R$ 222,59, embora tenha o menor volume com 1.880 unidades e receita de R$ 418.471,05.
Classificação: Os dados só sugerem

Limitações: Os dados não indicam as causas do baixo volume de vendas na categoria Esporte e no canal marketplace; dados adicionais de pesquisa de mercado e comportamento do consumidor ajudariam a confirmar os motivos dessas posições.

## Verificação automática dos números

Todos os números do relatório existem nas métricas. A checagem não verifica se cada número está ligado ao assunto certo, então a revisão humana continua necessária.

## Registro do orquestrador

Sequência de ferramentas escolhida pelo modelo:

1. validar_base
2. analisar_metricas
3. gerar_recomendacoes
4. verificar_numeros
