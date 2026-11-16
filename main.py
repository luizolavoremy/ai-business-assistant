from datetime import date

from analise import diagnostico_base_suja, metricas_base_limpa
from agentes import agente_validacao, agente_analise, agente_recomendacoes


def gerar_relatorio(base_suja, base_limpa, saida):
    print("1/3 Validando a base...")
    diagnostico = diagnostico_base_suja(base_suja)
    validacao = agente_validacao(diagnostico)

    print("2/3 Analisando as métricas...")
    metricas = metricas_base_limpa(base_limpa)
    analise = agente_analise(metricas)

    print("3/3 Gerando recomendações...")
    recomendacoes = agente_recomendacoes(validacao, analise)

    relatorio = (
        f"# Relatório de pedidos\n\nGerado em {date.today():%d/%m/%Y}.\n\n"
        "A validação (seção 1) analisa a base original, ainda suja. "
        "A análise e as recomendações (seções 2 e 3) usam a base já limpa no projeto 1.\n\n"
        f"## 1. Validação dos dados\n\n{validacao}\n\n"
        f"## 2. Análise comercial\n\n{analise}\n\n"
        f"## 3. Recomendações\n\n{recomendacoes}\n"
    )

    with open(saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)
    print(f"Relatório salvo em {saida}")


if __name__ == "__main__":
    gerar_relatorio("pedidos_loja.csv", "pedidos_limpos.csv", "relatorio.md")