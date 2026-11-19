from datetime import date

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agentes import MODELO, agente_analise, agente_recomendacoes, agente_validacao
from analise import diagnostico_base_suja, metricas_base_limpa
from verificacao import numeros_sem_origem

load_dotenv()
client = genai.Client()

BASE_SUJA = "pedidos_loja.csv"
BASE_LIMPA = "pedidos_limpos.csv"

estado = {}
registro = []


def validar_base() -> str:
    """Valida a base original de pedidos, ainda suja, e devolve a lista de problemas de qualidade encontrados."""
    registro.append("validar_base")
    estado["diagnostico"] = diagnostico_base_suja(BASE_SUJA)
    estado["validacao"] = agente_validacao(estado["diagnostico"])
    return estado["validacao"]


def analisar_metricas() -> str:
    """Calcula as métricas da base de pedidos já limpa e devolve a análise comercial em texto."""
    registro.append("analisar_metricas")
    estado["metricas"] = metricas_base_limpa(BASE_LIMPA)
    estado["analise"] = agente_analise(estado["metricas"])
    return estado["analise"]


def gerar_recomendacoes() -> str:
    """Gera as recomendações comerciais. Só funciona depois de validar_base e analisar_metricas."""
    registro.append("gerar_recomendacoes")
    if "validacao" not in estado or "analise" not in estado:
        return "ERRO: chame validar_base e analisar_metricas antes."
    estado["recomendacoes"] = agente_recomendacoes(estado["validacao"], estado["analise"])
    return estado["recomendacoes"]


def _conferir():
    todos = {"metricas": estado["metricas"], "diagnostico": estado["diagnostico"]}
    return {
        "validacao": numeros_sem_origem(estado["validacao"], estado["diagnostico"]),
        "analise": numeros_sem_origem(estado["analise"], estado["metricas"]),
        "recomendacoes": numeros_sem_origem(estado["recomendacoes"], todos),
    }


def verificar_numeros() -> str:
    """Confere se os números dos três textos existem nos dados. Devolve OK ou os números sem origem de cada texto."""
    registro.append("verificar_numeros")
    faltando = [c for c in ("validacao", "analise", "recomendacoes") if c not in estado]
    if faltando:
        return "ERRO: ainda faltam estas etapas: " + ", ".join(faltando)
    problemas = _conferir()
    if not any(problemas.values()):
        return "OK: todos os números existem nos dados."
    partes = [f"{texto}: {', '.join(nums)}" for texto, nums in problemas.items() if nums]
    return "NÚMEROS SEM ORIGEM em " + "; ".join(partes)


INSTRUCAO = """
Você é o orquestrador de um sistema que gera um relatório de pedidos. Você tem 4 ferramentas: validar_base, analisar_metricas, gerar_recomendacoes e verificar_numeros.

Objetivo: obter a validação dos dados, a análise comercial e as recomendações, e confirmar que os números estão corretos.

Regras:
- gerar_recomendacoes só pode ser chamada depois de validar_base e analisar_metricas.
- Depois de gerar as recomendações, chame verificar_numeros.
- Se a verificação apontar números sem origem na análise, chame analisar_metricas de novo, depois gerar_recomendacoes de novo, e verifique outra vez.
- Se apontar números sem origem só nas recomendações, chame apenas gerar_recomendacoes de novo e verifique outra vez.
- Se apontar números sem origem só na validação, chame validar_base de novo, depois gerar_recomendacoes de novo, e verifique outra vez.
- Refaça no máximo 2 vezes. Depois disso, pare, mesmo que ainda haja números suspeitos.
- Não reescreva nem resuma os textos das ferramentas. Ao terminar, responda com uma frase dizendo o que foi feito.
"""


def orquestrar(saida="relatorio_v2.md"):
    config = types.GenerateContentConfig(
        system_instruction=INSTRUCAO,
        tools=[validar_base, analisar_metricas, gerar_recomendacoes, verificar_numeros],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=12
        ),
    )
    resposta = client.models.generate_content(
        model=MODELO,
        contents="Gere o relatório de pedidos.",
        config=config,
    )
    print(resposta.text or "(o modelo terminou sem texto final)")

    faltando = [c for c in ("validacao", "analise", "recomendacoes") if c not in estado]
    if faltando:
        print("O orquestrador não completou: faltam " + ", ".join(faltando))
        return

    suspeitos = [n for lista in _conferir().values() for n in lista]
    if suspeitos:
        verificacao = "ATENÇÃO: números sem origem nas métricas: " + ", ".join(suspeitos)
    else:
        verificacao = (
            "Todos os números do relatório existem nas métricas. "
            "A checagem não verifica se cada número está ligado ao assunto certo, "
            "então a revisão humana continua necessária."
        )
    print(verificacao)

    sequencia = "\n".join(f"{i}. {nome}" for i, nome in enumerate(registro, start=1))
    relatorio = (
        f"# Relatório de pedidos (orquestrador v2)\n\nGerado em {date.today():%d/%m/%Y}.\n\n"
        "A validação (seção 1) analisa a base original, ainda suja. "
        "A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.\n\n"
        f"## 1. Validação dos dados\n\n{estado['validacao']}\n\n"
        f"## 2. Análise comercial\n\n{estado['analise']}\n\n"
        f"## 3. Recomendações\n\n{estado['recomendacoes']}\n\n"
        f"## Verificação automática dos números\n\n{verificacao}\n\n"
        f"## Registro do orquestrador\n\nSequência de ferramentas escolhida pelo modelo:\n\n{sequencia}\n"
    )
    with open(saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)
    print(f"Relatório salvo em {saida}")


if __name__ == "__main__":
    orquestrar()