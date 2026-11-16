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
A operação registrou 4.871 pedidos e 9.665 unidades vendidas, alcançando uma receita total de R$ 2.081.332,37 entre janeiro de 2023 e dezembro de 2024. O crescimento das unidades vendidas em 2024 na comparação com 2023 foi de 35,04%.

2. Categorias
A categoria Eletronicos registrou 2.527 unidades e R$ 821.515,52 de receita. A categoria Moda obteve 2.333 unidades e R$ 416.218,29 de receita. A categoria Casa & Decoracao somou 1.907 unidades e R$ 326.748,39 de receita, enquanto a categoria Beleza apresentou 1.560 unidades e R$ 385.033,10 de receita. Por fim, a categoria Esporte contabilizou 1.338 unidades e R$ 131.817,07 de receita. As categorias Beleza e Casa & Decoracao mudam de posição entre unidades e receita.

3. Ticket médio
O ticket médio da categoria Eletronicos foi de R$ 325,10. O ticket médio da categoria Beleza foi de R$ 246,82. O ticket médio da categoria Moda foi de R$ 178,40. O ticket médio da categoria Casa & Decoracao foi de R$ 171,34. O ticket médio da categoria Esporte foi de R$ 98,52.

4. Estados
Os estados de SP, RJ e MG ocupam as três primeiras posições em unidades vendidas, enquanto GO figura como o último colocado no ranking de unidades. O ticket médio é parecido entre os estados, variando entre R$ 199,73 e R$ 221,51.

5. Canais
O canal site registrou 4.384 unidades, R$ 947.832,27 de receita e ticket médio de R$ 216,20. O canal app obteve 3.401 unidades, R$ 715.029,05 de receita e ticket médio de R$ 210,24. O canal marketplace contabilizou 1.880 unidades, R$ 418.471,05 de receita e ticket médio de R$ 222,59. A diferença de ticket médio entre os canais é pequena.

6. Cancelamento
A taxa de cancelamento geral da operação foi de 7,92%. Por categoria, as taxas de cancelamento foram de 8,45% em Eletronicos, 7,95% em Moda, 7,88% em Beleza, 6,70% em Casa & Decoracao e 8,66% em Esporte.

7. Sazonalidade
Os três meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades. Os três meses mais fracos em unidades vendidas foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: Os dados consolidados de unidades e receita cobrem os 24 meses do período, não permitindo isolar o desempenho financeiro exclusivo do ano de 2024.

## 3. Recomendações

1. Separe para revisão 21 linhas com preço unitário negativo, 45 com quantidade zero ou negativa e 71 com preço unitário nulo, e remova 118 linhas duplicadas, pois os dados provam.
2. Mantenha a categoria Eletronicos liderando em unidades (2.527), receita (R$ 821.515,52) e ticket médio (R$ 325,10), pois os dados provam.
3. Investigue a categoria Esporte com 1.338 unidades na última posição, receita de R$ 131.817,07 e ticket médio de R$ 98,52, pois os dados só sugerem.
4. Investigue a categoria Beleza com ticket médio de R$ 246,82, sendo o 2º maior entre as categorias, e 1.560 unidades na 4ª posição em unidades, sendo uma hipótese que o volume menor pode ter causas que os dados não mostram, pois os dados só sugerem.

Limitações: Falta de dados de custos e margens por categoria, e dados adicionais de tráfego ajudariam a aprofundar a análise.
