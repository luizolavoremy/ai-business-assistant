# Relatório de pedidos

Gerado em 16/11/2026.

A validação (seção 1) analisa a base original, ainda suja. A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.

## 1. Validação dos dados

1. Gravidade: Alta
Problema: Preço unitário negativo
Quantidade encontrada: 21
Ação recomendada: Separar as linhas para revisão.

2. Gravidade: Alta
Problema: Quantidade zero ou negativa
Quantidade encontrada: 45
Ação recomendada: Separar as linhas para revisão.

3. Gravidade: Alta
Problema: Preço unitário nulo
Quantidade encontrada: 71
Ação recomendada: Separar as linhas para revisão.

4. Gravidade: Alta
Problema: Linhas duplicadas
Quantidade encontrada: 118
Ação recomendada: Remover as linhas duplicadas.

5. Gravidade: Média
Problema: Frete como texto
Quantidade encontrada: 5.118
Ação recomendada: Converter o frete para o formato numérico.

6. Gravidade: Média
Problema: Datas em formato BR misturadas com AAAA-MM-DD
Quantidade encontrada: 1.292
Ação recomendada: Padronizar as datas para o formato AAAA-MM-DD.

7. Gravidade: Média
Problema: Variações de texto na coluna cidade
Quantidade encontrada: 52 valores distintos, 12 após padronizar
Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços.

8. Gravidade: Média
Problema: Variações de texto na coluna categoria
Quantidade encontrada: 15 valores distintos, 5 após padronizar
Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços.

9. Gravidade: Média
Problema: Variações de texto na coluna status
Quantidade encontrada: 12 valores distintos, 4 após padronizar
Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços.

10. Gravidade: Baixa
Problema: Estado nulo
Quantidade encontrada: 163
Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base.

11. Gravidade: Baixa
Problema: Categoria nula
Quantidade encontrada: 56
Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base.

12. Gravidade: Baixa
Problema: Cidade nula
Quantidade encontrada: 31
Ação recomendada: Recuperar a cidade a partir do estado quando o estado tiver uma única cidade na base; caso contrário, separar as linhas para revisão.

Total de problemas listados: 12
A base não está pronta para análise.

## 2. Análise comercial

1. Visão geral
A operação registrou 4.871 pedidos e 9.665 unidades vendidas, totalizando uma receita total de R$ 2.081.332,37 entre janeiro de 2023 e dezembro de 2024. O crescimento das unidades vendidas em 2024 na comparação com 2023 foi de 35,04%.

2. Categorias
A categoria Eletronicos registrou 2.527 unidades e receita de R$ 821.515,52. A categoria Moda obteve 2.333 unidades e receita de R$ 416.218,29. A categoria Beleza somou 1.560 unidades e receita de R$ 385.033,10. A categoria Casa & Decoracao apresentou 1.907 unidades e receita de R$ 326.748,39. A categoria Esporte alcançou 1.338 unidades e receita de R$ 131.817,07. As categorias Beleza e Casa & Decoracao mudam de posição entre unidades e receita.

3. Ticket médio
O ticket médio da categoria Eletronicos é de R$ 325,10, o da categoria Beleza é de R$ 246,82, o da categoria Moda é de R$ 178,40, o da categoria Casa & Decoracao é de R$ 171,34 e o da categoria Esporte é de R$ 98,52.

4. Estados
Os primeiros colocados em unidades são SP com 3.405 unidades, RJ com 1.150 unidades e MG com 995 unidades, enquanto o último colocado entre os dez listados é GO com 341 unidades. O ticket médio é parecido entre os estados, variando entre R$ 199,73 e R$ 221,51.

5. Canais
O canal site registrou 4.384 unidades, receita de R$ 947.832,27 e ticket médio de R$ 216,20. O canal app obteve 3.401 unidades, receita de R$ 715.029,05 e ticket médio de R$ 210,24. O canal marketplace alcançou 1.880 unidades, receita de R$ 418.471,05 e ticket médio de R$ 222,59. A diferença de ticket médio entre os canais é pequena.

6. Cancelamento
A taxa geral de cancelamento é de 7,92%. Por categoria, as taxas de cancelamento são de 8,45% em Eletronicos, 7,95% em Moda, 7,88% em Beleza, 6,70% em Casa & Decoracao e 8,66% em Esporte.

7. Sazonalidade
Os 3 meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades. Os 3 meses mais fracos foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: Os dados cobrem apenas 10 estados e não detalham o motivo das variações mensais de vendas.

## 3. Recomendações

1. Separe para revisão 21 linhas com preço unitário negativo, 45 com quantidade zero ou negativa e 71 com preço unitário nulo, e remova 118 linhas duplicadas, pois os dados provam.
2. Mantenha a categoria Eletronicos, pois lidera em unidades (2.527), receita (R$ 821.515,52) e ticket médio (R$ 325,10), e os dados provam.
3. Investigue a categoria Esporte, que apresenta unidades: 1.338 (última posição), receita: R$ 131.817,07 e ticket médio: R$ 98,52, sendo que os dados só sugerem.
4. Investigue a categoria Beleza, que possui ticket médio: R$ 246,82 (2º maior entre as categorias) e unidades: 1.560 (4ª posição em unidades), e é uma hipótese que o volume menor pode ter causas que os dados não mostram, pois os dados só sugerem.

Limitações: Falta de dados de custos e margens por categoria, e dados adicionais de tráfego ajudariam a compreender melhor a rentabilidade e o comportamento de consumo.

## Verificação automática dos números

Todos os números do relatório existem nas métricas. A checagem não verifica se cada número está ligado ao assunto certo, então a revisão humana continua necessária.
