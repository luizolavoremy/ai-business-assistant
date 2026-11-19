# Relatório de pedidos (orquestrador v2)

Gerado em 19/11/2026.

A validação (seção 1) analisa a base original, ainda suja. A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.

## 1. Validação dos dados

1. Gravidade: Alta
- Problema: Preços unitários negativos
- Quantidade: 21
- Ação: Separar as linhas para revisão

2. Gravidade: Alta
- Problema: Quantidades de pedidos com valor zero ou negativo
- Quantidade: 45
- Ação: Separar as linhas para revisão

3. Gravidade: Alta
- Problema: Preços unitários ausentes (valores nulos)
- Quantidade: 71
- Ação: Separar as linhas para revisão

4. Gravidade: Média
- Problema: Frete cadastrado como texto (contendo "R$" e vírgula) em todas as linhas
- Quantidade: 5118
- Ação: Converter os valores de texto para formato numérico

5. Gravidade: Média
- Problema: Datas em formato brasileiro (DD/MM/AAAA) misturadas com o formato padrão (AAAA-MM-DD)
- Quantidade: 1292
- Ação: Padronizar todas as datas para o formato AAAA-MM-DD

6. Gravidade: Média
- Problema: Linhas duplicadas idênticas a outras já existentes
- Quantidade: 118
- Ação: Remover as linhas duplicadas

7. Gravidade: Baixa
- Problema: Variações inconsistentes de texto na coluna de status
- Quantidade: 12 valores distintos, 4 após padronizar
- Ação: Padronizar os valores ignorando maiúsculas, acentos e espaços

8. Gravidade: Baixa
- Problema: Variações inconsistentes de texto na coluna de categoria
- Quantidade: 15 valores distintos, 5 após padronizar
- Ação: Padronizar os valores ignorando maiúsculas, acentos e espaços

9. Gravidade: Baixa
- Problema: Categoria de produto ausente (valor nulo)
- Quantidade: 56
- Ação: Recuperar os valores a partir de outras colunas da própria base

10. Gravidade: Baixa
- Problema: Variações inconsistentes de texto na coluna de cidade
- Quantidade: 52 valores distintos, 12 após padronizar
- Ação: Padronizar os valores ignorando maiúsculas, acentos e espaços

11. Gravidade: Baixa
- Problema: Estado ausente (valor nulo)
- Quantidade: 163
- Ação: Recuperar os valores a partir de outras colunas da própria base

12. Gravidade: Baixa
- Problema: Cidade ausente (valor nulo)
- Quantidade: 31
- Ação: Recuperar os valores a partir do estado quando o estado tiver uma única cidade na base, ou separar as linhas para revisão caso contrário

Total de problemas listados: 12

A base não está pronta para análise e requer tratamento dos problemas identificados antes de ser utilizada.

## 2. Análise comercial

1. Visão geral: A loja registrou um total de 4.871 pedidos, com 9.665 unidades vendidas e uma receita total de R$ 2.081.332,37 entre os anos de 2023 e 2024. O crescimento das unidades vendidas em 2024 na comparação com 2023 foi de 35,04%.

2. Categorias: A categoria Eletrônicos registrou 2.527 unidades e R$ 821.515,52 de receita, Moda teve 2.333 unidades e R$ 416.218,29, Casa & Decoração obteve 1.907 unidades e R$ 326.748,39, Beleza somou 1.560 unidades e R$ 385.033,10, e Esporte alcançou 1.338 unidades e R$ 131.817,07. As categorias Beleza e Casa & Decoração mudam de posição entre unidades e receita.

3. Ticket médio: O ticket médio da categoria Eletrônicos foi de R$ 325,10, o de Beleza foi de R$ 246,82, o de Moda foi de R$ 178,40, o de Casa & Decoração foi de R$ 171,34 e o de Esporte foi de R$ 98,52.

4. Estados: Os três primeiros colocados em unidades foram SP com 3.405 unidades, RJ com 1.150 unidades e MG com 995 unidades, enquanto o último colocado entre os dez listados foi GO com 341 unidades. O ticket médio é parecido entre os estados, variando de R$ 199,73 em PE até R$ 221,51 em BA.

5. Canais: O canal site registrou 4.384 unidades, R$ 947.832,27 de receita e ticket médio de R$ 216,20, o app somou 3.401 unidades, R$ 715.029,05 de receita e ticket médio de R$ 210,24, e o marketplace obteve 1.880 unidades, R$ 418.471,05 de receita e ticket médio de R$ 222,59, destacando o marketplace com o maior ticket médio.

6. Cancelamento: A taxa de cancelamento geral foi de 7,92%, sendo de 8,45% em Eletrônicos, 7,95% em Moda, 7,88% em Beleza, 6,70% em Casa & Decoração e 8,66% em Esporte.

7. Sazonalidade: Os 3 meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades. Os 3 meses mais fracos foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: Os dados consolidados de estados cobrem apenas os dez principais estados listados no resumo, deixando de fora eventuais vendas de outras localidades.

## 3. Recomendações

1. Implemente o tratamento dos dados corrompidos separando para revisão as 21 linhas com preços unitários negativos, as 45 linhas com quantidades zero ou negativas e as 71 linhas com preços unitários ausentes, além de converter os 5.118 valores de frete de texto para formato numérico.
Classificação: Os dados provam

2. Mantenha o foco de investimento e estratégias de vendas na categoria Eletrônicos, que lidera o desempenho geral ao registrar 2.527 unidades e R$ 821.515,52 de receita.
Classificação: Os dados provam

3. Investigue as razões do desempenho fraco da categoria Esporte, que apresenta o menor volume com 1.338 unidades e a menor receita de R$ 131.817,07, além da maior taxa de cancelamento de 8,66%. Hipótese: o baixo desempenho pode estar relacionado à falta de atratividade do mix de produtos ou problemas logísticos. Dados adicionais necessários para confirmar: pesquisa de satisfação dos clientes e análise detalhada de devoluções por defeito.
Classificação: Os dados só sugerem

4. Invista em ações de crescimento para o canal marketplace, que apresenta o maior ticket médio de R$ 222,59, superando o site com R$ 216,20 e o app com R$ 210,24, apesar de registrar um volume menor de 1.880 unidades. Hipótese: o canal atrai um público com maior poder aquisitivo ou busca por produtos de maior valor agregado. Dados adicionais necessários para confirmar: perfil demográfico e histórico de navegação dos compradores por canal.
Classificação: Os dados só sugerem

Limitações: Os dados consolidados de estados cobrem apenas os dez principais estados listados no resumo, deixando de fora eventuais vendas de outras localidades. Dados adicionais necessários para confirmar: base completa com o universo total de estados e cidades atendidas.
Classificação: Os dados provam

## Verificação automática dos números

Todos os números do relatório existem nas métricas. A checagem não verifica se cada número está ligado ao assunto certo, então a revisão humana continua necessária.

## Registro do orquestrador

Sequência de ferramentas escolhida pelo modelo:

1. validar_base
2. analisar_metricas
3. gerar_recomendacoes
4. verificar_numeros
