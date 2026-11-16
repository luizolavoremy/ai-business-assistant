# Relatório de pedidos

Gerado em 16/11/2026.

A validação (seção 1) analisa a base original, ainda suja. A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.

## 1. Validação dos dados

1. **Gravidade: Alta**
   - Problema: Preço unitário negativo
   - Quantidade encontrada: 21
   - Ação recomendada: Separar as linhas para revisão

2. **Gravidade: Alta**
   - Problema: Quantidade zero ou negativa
   - Quantidade encontrada: 45
   - Ação recomendada: Separar as linhas para revisão

3. **Gravidade: Alta**
   - Problema: Preço unitário nulo
   - Quantidade encontrada: 71
   - Ação recomendada: Separar as linhas para revisão

4. **Gravidade: Média**
   - Problema: Linhas duplicadas
   - Quantidade encontrada: 118
   - Ação recomendada: Remover as linhas duplicadas

5. **Gravidade: Média**
   - Problema: Datas em formato BR (DD/MM/AAAA) misturadas com AAAA-MM-DD
   - Quantidade encontrada: 1292
   - Ação recomendada: Padronizar o formato de todas as datas para AAAA-MM-DD

6. **Gravidade: Média**
   - Problema: Frete como texto (com "R$" e vírgula)
   - Quantidade encontrada: 5118
   - Ação recomendada: Converter os valores de frete para o formato numérico

7. **Gravidade: Baixa**
   - Problema: Estado nulo
   - Quantidade encontrada: 163
   - Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base

8. **Gravidade: Baixa**
   - Problema: Categoria nula
   - Quantidade encontrada: 56
   - Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base

9. **Gravidade: Baixa**
   - Problema: Cidade nula
   - Quantidade encontrada: 31
   - Ação recomendada: Recuperar a cidade a partir do estado quando o estado tiver uma única cidade na base; caso contrário, separar as linhas para revisão

10. **Gravidade: Baixa**
    - Problema: Variações de texto na coluna cidade
    - Quantidade encontrada: 52 valores distintos, 12 após padronizar
    - Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços

11. **Gravidade: Baixa**
    - Problema: Variações de texto na coluna categoria
    - Quantidade encontrada: 15 valores distintos, 5 após padronizar
    - Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços

12. **Gravidade: Baixa**
    - Problema: Variações de texto na coluna status
    - Quantidade encontrada: 12 valores distintos, 4 após padronizar
    - Ação recomendada: Padronizar os textos ignorando maiúsculas, acentos e espaços

Total de problemas listados: 12
A base não está pronta para análise.

## 2. Análise comercial

1. Visão geral: A operação registrou 4.871 total de pedidos, 9.665 unidades vendidas e uma receita total de R$ 2.081.332,37. As unidades vendidas apresentaram um crescimento de 35,04% em 2024 sobre 2023.

2. Categorias: A categoria Eletronicos registrou 2.527 unidades e R$ 821.515,52 de receita, Moda teve 2.333 unidades e R$ 416.218,29 de receita, Casa & Decoracao somou 1.907 unidades e R$ 326.748,39 de receita, Beleza teve 1.560 unidades e R$ 385.033,10 de receita, e Esporte alcançou 1.338 unidades e R$ 131.817,07 de receita. As categorias Beleza e Casa & Decoracao mudam de posição entre unidades e receita.

3. Ticket médio: O ticket médio da categoria Eletronicos foi de R$ 325,10, o de Moda foi de R$ 178,40, o de Casa & Decoracao foi de R$ 171,34, o de Beleza foi de R$ 246,82 e o de Esporte foi de R$ 98,52.

4. Estados: Os primeiros colocados em unidades foram SP com 3.405 unidades, RJ com 1.150 unidades e MG com 995 unidades, enquanto o último colocado foi GO com 341 unidades. O ticket médio é parecido entre os estados, variando de R$ 199,73 a R$ 221,51.

5. Canais: O canal site registrou 4.384 unidades, R$ 947.832,27 de receita e ticket médio de R$ 216,20, o app teve 3.401 unidades, R$ 715.029,05 de receita e ticket médio de R$ 210,24, e o marketplace somou 1.880 unidades, R$ 418.471,05 de receita e ticket médio de R$ 222,59, destacando o marketplace com o maior ticket médio.

6. Cancelamento: A taxa de cancelamento geral foi de 7,92%, sendo de 8,45% em Eletronicos, 7,95% em Moda, 7,88% em Beleza, 6,70% em Casa & Decoracao e 8,66% em Esporte.

7. Sazonalidade: Os 3 meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades, enquanto os 3 mais fracos foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: O volume por estado não mostra poder de compra por pessoa, apenas o total vendido em cada região.

## 3. Recomendações

1. Mantenha o investimento na categoria Eletronicos, pois ela registrou 2.527 unidades, R$ 821.515,52 de receita e ticket médio de R$ 325,10, liderando em todas as métricas. Os dados provam.

2. Separe as 21 linhas com preço unitário negativo, as 45 linhas com quantidade zero ou negativa e as 71 linhas com preço unitário nulo para revisão. Os dados provam.

3. Invista no canal marketplace para impulsionar suas unidades, pois ele registrou o maior ticket médio de R$ 222,59, apesar de ter somado 1.880 unidades, ficando abaixo dos demais canais. Os dados só sugerem.

4. Investigue os motivos do desempenho da categoria Esporte, que alcançou 1.338 unidades e R$ 131.817,07 de receita, além de apresentar taxa de cancelamento de 8,66% e ticket médio de R$ 98,52. Os dados só sugerem.

Limitações: O volume por estado não mostra poder de compra por pessoa, apenas o total vendido em cada região; dados adicionais de custos operacionais e pesquisas de satisfação ajudariam a confirmar as causas do cancelamento e do volume menor em canais e categorias.
