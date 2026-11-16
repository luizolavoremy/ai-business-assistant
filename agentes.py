import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from analise import diagnostico_base_suja

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

FORMATO DA RESPOSTA:
Lista numerada, ordenada da maior gravidade para a menor, com até 10 itens. Cada item deve ter: gravidade (alta, média ou baixa), o problema, a quantidade encontrada e a ação recomendada. Termine com uma frase dizendo se a base está pronta para análise.
"""


def agente_validacao(diagnostico):
    conteudo = json.dumps(diagnostico, ensure_ascii=False)
    return chamar_modelo(PROMPT_VALIDACAO, conteudo)


if __name__ == "__main__":
    diagnostico = diagnostico_base_suja("pedidos_loja.csv")
    print(agente_validacao(diagnostico))