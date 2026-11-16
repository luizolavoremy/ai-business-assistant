# Relatório de pedidos

Gerado em 16/11/2026.

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
   - Problema: Frete como texto (mistura "R$" e vírgula)
   - Quantidade encontrada: 5118
   - Ação recomendada: Converter os valores de frete para o formato numérico

6. **Gravidade: Média**
   - Problema: Datas em formato BR (DD/MM/AAAA) misturadas com o formato AAAA-MM-DD
   - Quantidade encontrada: 1292
   - Ação recomendada: Padronizar todas as datas para o formato AAAA-MM-DD

7. **Gravidade: Média**
   - Problema: Variações de texto na coluna cidade
   - Quantidade encontrada: 52 valores distintos, 12 após padronizar
   - Ação recomendada: Padronizar os valores da coluna cidade ignorando maiúsculas, acentos e espaços

8. **Gravidade: Média**
   - Problema: Variações de texto na coluna status
   - Quantidade encontrada: 12 valores distintos, 4 após padronizar
   - Ação recomendada: Padronizar os valores da coluna status ignorando maiúsculas, acentos e espaços

9. **Gravidade: Média**
   - Problema: Variações de texto na coluna categoria
   - Quantidade encontrada: 15 valores distintos, 5 após padronizar
   - Ação recomendada: Padronizar os valores da coluna categoria ignorando maiúsculas, acentos e espaços

10. **Gravidade: Baixa**
    - Problema: Estado nulo
    - Quantidade encontrada: 163
    - Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base

11. **Gravidade: Baixa**
    - Problema: Categoria nula
    - Quantidade encontrada: 56
    - Ação recomendada: Recuperar esses valores a partir de outras colunas da própria base

12. **Gravidade: Baixa**
    - Problema: Cidade nula
    - Quantidade encontrada: 31
    - Ação recomendada: Recuperar esses valores a partir do estado quando o estado tiver uma única cidade na base, ou separar as linhas para revisão caso contrário

Total de problemas listados: 12
A base não está pronta para análise.

## 2. Análise comercial

1. Visão geral: A operação registrou um total de 4.871 pedidos, com 9.665 unidades vendidas e uma receita total de R$ 2.081.332,37. O crescimento das unidades vendidas em 2024 na comparação com 2023 foi de 35,04%.

2. Categorias: A categoria Eletronicos registrou 2.527 unidades e receita de R$ 821.515,52. Moda teve 2.333 unidades e receita de R$ 416.218,29, Casa & Decoracao somou 1.907 unidades e receita de R$ 326.748,39, Beleza alcançou 1.560 unidades e receita de R$ 385.033,1, e Esporte apresentou 1.338 unidades e receita de R$ 131.817,07. As categorias Beleza e Casa & Decoracao mudam de posição entre unidades e receita.

3. Ticket médio: O ticket médio foi de R$ 325,1 em Eletronicos, R$ 246,82 em Beleza, R$ 178,4 em Moda, R$ 171,34 em Casa & Decoracao e R$ 98,52 em Esporte.

4. Estados: Os três primeiros colocados em unidades foram SP com 3.405 unidades, RJ com 1.150 unidades e MG com 995 unidades, enquanto o último colocado entre os listados foi GO com 341 unidades. O ticket médio é bastante parecido entre os estados, variando de R$ 199,73 em PE a R$ 221,51 em BA.

5. Canais: O canal site registrou 4.384 unidades, receita de R$ 947.832,27 e ticket médio de R$ 216,2. O app somou 3.401 unidades, receita de R$ 715.029,05 e ticket médio de R$ 210,24, ao passo que o marketplace obteve 1.880 unidades, receita de R$ 418.471,05 e o maior ticket médio, de R$ 222,59.

6. Cancelamento: A taxa de cancelamento geral da operação foi de 7,92%. Por categoria, a taxa de cancelamento foi de 8,66% em Esporte, 8,45% em Eletronicos, 7,95% em Moda, 7,88% em Beleza e 6,7% em Casa & Decoracao.

7. Sazonalidade: Os três meses mais fortes em unidades vendidas foram 2024-11 com 825 unidades, 2024-12 com 720 unidades e 2023-11 com 552 unidades. Os três meses mais fracos foram 2023-02 com 226 unidades, 2023-01 com 235 unidades e 2023-08 com 300 unidades.

Limitações: Os dados consolidados não detalham o perfil demográfico dos clientes por estado ou canal de aquisição.

## 3. Recomendações

1. Separe para revisão 21 linhas com preço unitário negativo, 45 linhas com quantidade zero ou negativa e 71 linhas com preço unitário nulo, conforme indicado nos problemas 1, 2 e 3 da validação de dados. Classificação: Os dados provam.

2. Mantenha o investimento na categoria Eletronicos, pois ela lidera todas as métricas com 2.527 unidades, receita de R$ 821.515,52 e ticket médio de R$ 325,10, conforme os itens 2 e 3 da análise comercial. Classificação: Os dados provam.

3. Investigue o desempenho da categoria Esporte, que apresentou o menor volume com 1.338 unidades, menor receita de R$ 131.817,07, menor ticket médio de R$ 98,52 e a maior taxa de cancelamento de 8,66%, conforme os itens 2, 3 e 6 da análise comercial. Classificação: Os dados só sugerem.

4. Invista no canal marketplace, que apresentou menor volume com 1.880 unidades, mas alcançou o maior ticket médio de R$ 222,59 e receita de R$ 418.471,05, conforme o item 5 da análise comercial. Classificação: Os dados só sugerem.

Limitações: Os dados consolidados não detalham os motivos dos cancelamentos por categoria nem o perfil de tráfego e conversão do canal marketplace; dados adicionais de pesquisas de pós-venda e de comportamento de navegação ajudariam a confirmar a causa do volume menor e da taxa de cancelamento.
