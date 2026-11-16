import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from analise import diagnostico_base_suja, formatar_para_modelo, metricas_base_limpa

load_dotenv()
client = genai.Client()

MODELO = "gemini-3.5-flash-lite"


def chamar_modelo(instrucao, conteudo, tentativas=5):
    for i in range(tentativas):
        try:
            resposta = client.models.generate_content(
                model=MODELO,
                contents=conteudo,
                config=types.GenerateContentConfig(
                    system_instruction=instrucao,
                    temperature=0,
                ),
            )
            return resposta.text
        except errors.ServerError as e:
            if i == tentativas - 1:
                raise
            espera = 2 ** i * 5  # 5s, 10s, 20s, 40s
            print(f"Modelo indisponível ({e.code}). Nova tentativa em {espera}s...")
            time.sleep(espera)


def _br(valor, casas):
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------------------
# 1. VALIDAÇÃO: gerada em Python, sem modelo
# ---------------------------------------------------------------------------

def agente_validacao(diag):
    nulos = diag["nulos_por_coluna"]
    itens = []

    def add(grav, problema, qtd, acao):
        if qtd:
            itens.append((grav, problema, qtd, acao))

    revisar = "Separar as linhas para revisão"
    add(0, "Preço unitário negativo", diag["preco_unitario_negativo"], revisar)
    add(0, "Quantidade zero ou negativa", diag["quantidade_zero_ou_negativa"], revisar)
    add(0, "Preço unitário nulo", nulos.get("preco_unitario", 0), revisar)
    add(0, "Linhas duplicadas", diag["linhas_duplicadas"], "Remover as linhas duplicadas")
    add(1, "Frete como texto", diag["frete_como_texto"],
        "Converter o frete para o formato numérico")
    add(1, "Datas em formato BR misturadas com AAAA-MM-DD", diag["datas_em_formato_br"],
        "Padronizar as datas para o formato AAAA-MM-DD")
    for coluna in ("cidade", "categoria", "status"):
        v = diag[f"variacoes_{coluna}"]
        if v["valores_distintos"] != v["valores_apos_padronizar"]:
            qtd = (f"{_br(v['valores_distintos'], 0)} valores distintos, "
                   f"{_br(v['valores_apos_padronizar'], 0)} após padronizar")
            add(1, f"Variações de texto na coluna {coluna}", qtd,
                "Padronizar os textos ignorando maiúsculas, acentos e espaços")
    recuperar = "Recuperar esses valores a partir de outras colunas da própria base"
    add(2, "Estado nulo", nulos.get("estado", 0), recuperar)
    add(2, "Categoria nula", nulos.get("categoria", 0), recuperar)
    add(2, "Cidade nula", nulos.get("cidade", 0),
        "Recuperar a cidade a partir do estado quando o estado tiver uma única "
        "cidade na base; caso contrário, separar as linhas para revisão")

    nomes = ["Alta", "Média", "Baixa"]
    linhas = []
    for i, (grav, problema, qtd, acao) in enumerate(itens, 1):
        qtd_txt = qtd if isinstance(qtd, str) else _br(qtd, 0)
        linhas.append(
            f"{i}. Gravidade: {nomes[grav]}\n"
            f"Problema: {problema}\n"
            f"Quantidade encontrada: {qtd_txt}\n"
            f"Ação recomendada: {acao}.\n"
        )
    pronta = ("A base está pronta para análise." if not itens
              else "A base não está pronta para análise.")
    return "\n".join(linhas) + f"\nTotal de problemas listados: {len(itens)}\n{pronta}"


# ---------------------------------------------------------------------------
# 2. ANÁLISE: modelo
# ---------------------------------------------------------------------------

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
- Os números do JSON já vêm escritos no formato brasileiro, como texto, com duas casas decimais quando têm decimais. Copie-os exatamente, sem remover zeros nem alterar dígitos. Valores em reais levam "R$", como R$ 385.033,10.
- Para falar de ranking de categorias, estados e canais, use apenas posicao_unidades e posicao_receita. Para falar dos meses mais fortes e mais fracos, use apenas top3_meses e bottom3_meses. Nunca ordene nem compare valores por conta própria.
- Só aponte divergência entre unidades e receita quando posicao_unidades e posicao_receita forem diferentes, ou quando o ticket médio for bem diferente dos demais. Se as duas posições forem iguais, não use "mas" nem contraste.
- Os totais do JSON cobrem os 24 meses, 2023 e 2024 juntos. Nunca apresente esses totais como se fossem só de 2024.
- O período cobre 24 meses (janeiro de 2023 a dezembro de 2024). Nunca escreva "24 anos".
- Não afirme causas. Descreva o que os dados mostram e marque qualquer explicação como hipótese.
- Não exagere diferenças pequenas. Se os valores forem parecidos, diga que a diferença é pequena.
- Volume por estado não mostra poder de compra por pessoa, só o total vendido.
- Escreva "4.871 pedidos", e não "4.871 total de pedidos". Não copie o nome do campo do JSON para dentro da frase.
- Escreva os nomes das categorias exatamente como estão no JSON.
- Responda em português.

FORMATO DA RESPOSTA:
Escreva exatamente 7 achados numerados, nesta ordem:
1. Visão geral: total de pedidos, unidades, receita total e crescimento de 2024 sobre 2023.
2. Categorias: unidades e receita de cada categoria, e quais mudam de posição entre unidades e receita.
3. Ticket médio: o ticket médio de cada uma das 5 categorias.
4. Estados: os 3 primeiros e o último colocado em unidades, e se o ticket médio é parecido entre os estados. Se citar o intervalo do ticket médio, use só valores de por_estado, indicando o menor e o maior, sem mencionar canais.
5. Canais: unidades, receita e ticket médio dos 3 canais, e se a diferença de ticket médio entre eles é pequena ou relevante.
6. Cancelamento: a taxa geral e a taxa de cada uma das 5 categorias.
7. Sazonalidade: os 3 meses mais fortes e os 3 mais fracos.
Cada achado tem um título curto e 1 a 3 frases com os números. Depois, escreva uma linha começando com "Limitações:" que cite uma limitação dos dados.
"""


def agente_analise(metricas):
    conteudo = json.dumps(formatar_para_modelo(metricas), ensure_ascii=False)
    return chamar_modelo(PROMPT_ANALISE, conteudo)


# ---------------------------------------------------------------------------
# 3. RECOMENDAÇÕES: Python escolhe os grupos, o modelo só redige
# ---------------------------------------------------------------------------

def montar_fatos(diag, met):
    cats = met["por_categoria"]
    nulos = diag["nulos_por_coluna"]

    # líder: posição 1 em unidades; lista só as métricas em que ele é o 1º
    lider = next(n for n, c in cats.items() if c["posicao_unidades"] == 1)
    maior_ticket = max(c["ticket_medio"] for c in cats.values())
    metricas_lider = [f"unidades ({_br(cats[lider]['unidades'], 0)})"]
    if cats[lider]["posicao_receita"] == 1:
        metricas_lider.append(f"receita (R$ {_br(cats[lider]['receita'], 2)})")
    if cats[lider]["ticket_medio"] == maior_ticket:
        metricas_lider.append(f"ticket médio (R$ {_br(cats[lider]['ticket_medio'], 2)})")

    # mais fraco: última posição em unidades
    fraca = max(cats, key=lambda n: cats[n]["posicao_unidades"])
    f = cats[fraca]

    # crescimento: entre os 2 maiores tickets, 4ª posição ou pior em unidades, e não o mais fraco
    ordem_ticket = sorted(cats, key=lambda n: cats[n]["ticket_medio"], reverse=True)
    cresc = next(
        (n for n in ordem_ticket[:2] if cats[n]["posicao_unidades"] >= 4 and n != fraca),
        None,
    )

    revisar = (
        f"{_br(diag['preco_unitario_negativo'], 0)} linhas com preço unitário negativo, "
        f"{_br(diag['quantidade_zero_ou_negativa'], 0)} com quantidade zero ou negativa e "
        f"{_br(nulos.get('preco_unitario', 0), 0)} com preço unitário nulo"
    )

    fatos = [
        "AÇÃO 1 (qualidade dos dados). Comece com 'Separe'. "
        f"Separar para revisão: {revisar}. "
        f"Remover {_br(diag['linhas_duplicadas'], 0)} linhas duplicadas. "
        "Classificação: Os dados provam.",

        f"AÇÃO 2 (manter o líder). Comece com 'Mantenha'. Categoria: {lider}. "
        f"Lidera em: {', '.join(metricas_lider)}. Cite só essas métricas. "
        "Classificação: Os dados provam.",

        f"AÇÃO 3 (categoria mais fraca). Comece com 'Investigue'. Categoria: {fraca}. "
        f"Unidades: {_br(f['unidades'], 0)} (última posição). "
        f"Receita: R$ {_br(f['receita'], 2)}. "
        f"Ticket médio: R$ {_br(f['ticket_medio'], 2)}. "
        "Não cite taxa de cancelamento. Classificação: Os dados só sugerem.",
    ]

    if cresc:
        c = cats[cresc]
        pos_ticket = ordem_ticket.index(cresc) + 1
        fatos.append(
            f"AÇÃO 4 (crescimento). Comece com 'Investigue'. Categoria: {cresc}. "
            f"Ticket médio: R$ {_br(c['ticket_medio'], 2)} ({pos_ticket}º maior entre as categorias). "
            f"Unidades: {_br(c['unidades'], 0)} ({c['posicao_unidades']}ª posição em unidades). "
            "Explique que o volume menor pode ter causas que os dados não mostram (hipótese). "
            "Classificação: Os dados só sugerem."
        )
    else:
        fatos.append("AÇÃO 4: nenhuma categoria cumpre ticket alto com volume baixo. "
                     "Escreva só 3 ações.")

    return "\n".join(fatos)


PROMPT_RECOMENDACOES = """
PAPEL:
Você é um consultor de e-commerce que transforma fatos em ações práticas.

TAREFA:
Você recebe uma lista de FATOS, um bloco por ação. Escreva uma ação para cada bloco, na mesma ordem, usando só os números e o verbo de abertura indicados no bloco.

REGRAS:
- Escreva uma ação por bloco, sem juntar nem dividir blocos, e sem criar ações extras.
- Copie os números exatamente como estão nos fatos. Não faça contas nem cite números que não estejam nos fatos.
- Escreva os nomes das categorias exatamente como estão nos fatos.
- Não afirme causas. Quando o bloco indicar hipótese, diga que é uma hipótese.
- Não cite taxa de cancelamento, a menos que o bloco peça.
- Não invente valores de desconto, orçamento nem prazos.
- Responda em português.

FORMATO DA RESPOSTA:
Ações numeradas de 1 em diante. Cada ação tem uma frase com a ação, começando com o verbo indicado, seguida da justificativa com os números do bloco e da classificação ("Os dados provam" ou "Os dados só sugerem") ao final.
Depois, escreva uma linha começando com "Limitações:" que cite 1 a 2 limitações ligadas às ações acima, como falta de dados de custos, margens ou tráfego por categoria, e quais dados adicionais ajudariam.
"""


def agente_recomendacoes(validacao, analise, diagnostico=None, metricas=None):
    # main.py chama só com (validacao, analise); os dados são lidos aqui
    if diagnostico is None:
        diagnostico = diagnostico_base_suja("pedidos_loja.csv")
    if metricas is None:
        metricas = metricas_base_limpa("pedidos_limpos.csv")
    fatos = montar_fatos(diagnostico, metricas)
    return chamar_modelo(PROMPT_RECOMENDACOES, "FATOS:\n" + fatos)


if __name__ == "__main__":
    diagnostico = diagnostico_base_suja("pedidos_loja.csv")
    metricas = metricas_base_limpa("pedidos_limpos.csv")
    validacao = agente_validacao(diagnostico)
    analise = agente_analise(metricas)
    print(agente_recomendacoes(validacao, analise))