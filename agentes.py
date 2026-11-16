import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from analise import diagnostico_base_suja, metricas_base_limpa

load_dotenv()
client = genai.Client()

MODELO = "gemini-3.5-flash-lite"


def chamar_modelo(instrucao, conteudo):
    resposta = client.models.generate_content(
        model=MODELO,
        contents=conteudo,
        config=types.GenerateContentConfig(system_instruction=instrucao),
    )
    return resposta.text


PROMPT_VALIDACAO = """
PAPEL:
Você é um analista de qualidade de dados especializado em bases de e-commerce.

TAREFA:
Você recebe um resumo em JSON com contagens de problemas encontrados numa base de pedidos de loja online que ainda não foi limpa. Interprete esse resumo e liste os problemas de qualidade, do mais grave ao menos grave, dizendo o que fazer com cada um. Você só diagnostica: não corrige nem altera nenhum dado.

SIGNIFICADO DOS CAMPOS:
- total_linhas: número de linhas da base.
- linhas_duplicadas: linhas idênticas a outra já existente.
- nulos_por_coluna: quantidade de valores vazios, só nas colunas que têm algum.
- quantidade_zero_ou_negativa: pedidos com quantidade menor ou igual a zero.
- preco_unitario_negativo: pedidos com preço unitário negativo.
- datas_em_formato_br: datas escritas como DD/MM/AAAA. As demais estão em AAAA-MM-DD, então a coluna mistura dois formatos.
- frete_como_texto: valores de frete escritos como texto, com "R$" e vírgula, e não como número.
- variacoes_cidade, variacoes_categoria e variacoes_status: "valores_distintos" é quantos valores diferentes a coluna tem, e "valores_apos_padronizar" é quantos sobram ao ignorar maiúsculas, acentos e espaços. Se os dois números forem diferentes, o mesmo valor está escrito de formas diferentes.

REGRAS:
- Use apenas os números do JSON. Nunca invente valores nem problemas.
- Valor vazio em data_entrega é esperado quando o pedido foi cancelado ou ainda não foi entregue. Não trate isso como erro.
- Quando o valor correto não puder ser descoberto, como um preço ausente, recomende separar as linhas para revisão, e não preencher com estimativa.
- Responda em português.
- Estado e categoria vazios normalmente podem ser recuperados, porque cada cidade pertence a um único estado e cada produto pertence a uma única categoria. Recomende recuperar esses valores a partir de outras colunas da própria base, e não separar as linhas.
- Cidade vazia só pode ser recuperada a partir do estado quando o estado tem uma única cidade na base. Se o estado tiver mais de uma cidade, recomende separar as linhas para revisão.

FORMATO DA RESPOSTA:
Lista numerada, ordenada da maior gravidade para a menor, com todos os problemas encontrados, sem omitir nenhum. Cada item deve ter: gravidade (alta, média ou baixa), o problema, a quantidade encontrada e a ação recomendada. Escreva cada ação no imperativo, como "Separar as linhas para revisão". Não use a palavra "recomende" nem "recomendo" dentro da ação.
Depois da lista, escreva uma linha com o total de problemas listados, no formato "Total de problemas listados: N". Termine com uma frase dizendo se a base está pronta para análise.
Nos problemas de variação de texto, informe sempre os valores antes e depois de padronizar, por exemplo "12 valores distintos, 4 após padronizar". Nunca diga só que "há inconsistências".
"""


def agente_validacao(diagnostico):
    conteudo = json.dumps(diagnostico, ensure_ascii=False)
    return chamar_modelo(PROMPT_VALIDACAO, conteudo)


PROMPT_ANALISE = """
PAPEL:
Você é um analista comercial de e-commerce.

TAREFA:
Você recebe um resumo em JSON com métricas de pedidos de uma loja online, entre janeiro de 2023 e dezembro de 2024, calculadas a partir de uma base já limpa. Escreva os principais achados comerciais a partir desses números.

SIGNIFICADO DOS CAMPOS:
- total_pedidos: número de pedidos. unidades_vendidas: soma das quantidades, e um pedido pode ter até 4 unidades. Não confunda os dois.
- receita_total: soma de quantidade vezes preço unitário, em reais.
- taxa_cancelamento_pct: percentual de pedidos cancelados.
- crescimento_unidades_2024_vs_2023_pct: variação das unidades vendidas de 2023 para 2024.
- por_categoria, por_estado e por_canal: para cada grupo, unidades, receita, taxa_cancelamento_pct, ticket_medio (receita dividida por unidades), posicao_unidades e posicao_receita.
- posicao_unidades e posicao_receita: posição do grupo no ranking, sendo 1 o maior. Se as duas posições forem diferentes, o grupo troca de posição entre as métricas.
- top5_produtos_por_receita e bottom5_produtos_por_receita: os 5 maiores e os 5 menores produtos em receita.
- unidades_por_mes: unidades vendidas em cada mês.
- top3_meses e bottom3_meses: os 3 meses com mais e com menos unidades vendidas, já ordenados.

REGRAS:
- Use apenas os números do JSON e cite o número em cada achado. Nunca invente valores.
- Copie cada número exatamente como está no JSON, sem alterar nenhum dígito.
- Para falar de ranking de categorias, estados e canais, use apenas posicao_unidades e posicao_receita. Para falar dos meses mais fortes e mais fracos, use apenas top3_meses e bottom3_meses. Nunca ordene nem compare valores por conta própria.
- Só aponte divergência entre unidades e receita quando posicao_unidades e posicao_receita forem diferentes, ou quando o ticket médio for bem diferente dos demais. Se as duas posições forem iguais, não use "mas" nem contraste.
- Os totais do JSON cobrem os 24 meses, 2023 e 2024 juntos. Nunca apresente esses totais como se fossem só de 2024.
- Não afirme causas. Descreva o que os dados mostram e marque qualquer explicação como hipótese.
- Não exagere diferenças pequenas. Se os valores forem parecidos, diga que a diferença é pequena.
- Volume por estado não mostra poder de compra por pessoa, só o total vendido.
- Escreva valores em reais no formato brasileiro, como R$ 2.081.332,37.
- Responda em português.

FORMATO DA RESPOSTA:
Escreva exatamente 7 achados numerados, nesta ordem:
1. Visão geral: total de pedidos, unidades, receita total e crescimento de 2024 sobre 2023.
2. Categorias: unidades e receita de cada categoria, e quais mudam de posição entre unidades e receita.
3. Ticket médio: o ticket médio de cada uma das 5 categorias.
4. Estados: os 3 primeiros e o último colocado em unidades, e se o ticket médio é parecido entre os estados.
5. Canais: unidades, receita e ticket médio dos 3 canais, destacando o maior ticket médio.
6. Cancelamento: a taxa geral e a taxa de cada uma das 5 categorias.
7. Sazonalidade: os 3 meses mais fortes e os 3 mais fracos.
Cada achado tem um título curto e 1 a 3 frases com os números. Depois, escreva uma linha começando com "Limitações:" que cite uma limitação dos dados.
"""


def agente_analise(metricas):
    conteudo = json.dumps(metricas, ensure_ascii=False)
    return chamar_modelo(PROMPT_ANALISE, conteudo)


if __name__ == "__main__":
    metricas = metricas_base_limpa("pedidos_limpos.csv")
    print(agente_analise(metricas))