import json
import unicodedata

import pandas as pd


def _normalizar(texto):
    texto = texto.strip().lower()
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()


def _variacoes_de_texto(coluna):
    valores = coluna.dropna()
    return {
        "valores_distintos": int(valores.nunique()),
        "valores_apos_padronizar": int(valores.map(_normalizar).nunique()),
    }


def diagnostico_base_suja(caminho):
    df = pd.read_csv(caminho)

    nulos = df.isna().sum()
    nulos = {coluna: int(qtd) for coluna, qtd in nulos.items() if qtd > 0}

    return {
        "total_linhas": len(df),
        "linhas_duplicadas": int(df.duplicated().sum()),
        "nulos_por_coluna": nulos,
        "quantidade_zero_ou_negativa": int((df["quantidade"] <= 0).sum()),
        "preco_unitario_negativo": int((df["preco_unitario"] < 0).sum()),
        "datas_em_formato_br": int(df["data_pedido"].str.contains("/").sum()),
        "frete_como_texto": int(df["frete"].str.startswith("R$").sum()),
        "variacoes_cidade": _variacoes_de_texto(df["cidade"]),
        "variacoes_categoria": _variacoes_de_texto(df["categoria"]),
        "variacoes_status": _variacoes_de_texto(df["status"]),
    }


def _para_dict(dados):
    return json.loads(dados.to_json(orient="index"))


def _resumo_por(df, coluna):
    grupo = df.groupby(coluna).agg(
        unidades=("quantidade", "sum"),
        receita=("receita", "sum"),
        taxa_cancelamento_pct=("cancelado", "mean"),
    )
    grupo["receita"] = grupo["receita"].round(2)
    grupo["taxa_cancelamento_pct"] = (grupo["taxa_cancelamento_pct"] * 100).round(2)
    grupo["ticket_medio"] = (grupo["receita"] / grupo["unidades"]).round(2)
    return _para_dict(grupo.sort_values("receita", ascending=False))


def metricas_base_limpa(caminho):
    df = pd.read_csv(caminho)
    datas = pd.to_datetime(df["data_pedido"])
    df["mes"] = datas.dt.strftime("%Y-%m")
    df["ano"] = datas.dt.year
    df["cancelado"] = df["status"] == "Cancelado"

    unidades_por_ano = df.groupby("ano")["quantidade"].sum()
    crescimento = (unidades_por_ano[2024] / unidades_por_ano[2023] - 1) * 100

    receita_produto = df.groupby("produto")["receita"].sum().round(2)
    receita_produto = receita_produto.sort_values(ascending=False)

    return {
        "total_pedidos": len(df),
        "unidades_vendidas": int(df["quantidade"].sum()),
        "receita_total": round(float(df["receita"].sum()), 2),
        "taxa_cancelamento_pct": round(float(df["cancelado"].mean() * 100), 2),
        "crescimento_unidades_2024_vs_2023_pct": round(float(crescimento), 2),
        "por_categoria": _resumo_por(df, "categoria"),
        "por_estado": _resumo_por(df, "estado"),
        "por_canal": _resumo_por(df, "canal"),
        "top5_produtos_por_receita": _para_dict(receita_produto.head(5)),
        "bottom5_produtos_por_receita": _para_dict(receita_produto.tail(5)),
        "unidades_por_mes": _para_dict(df.groupby("mes")["quantidade"].sum()),
    }


if __name__ == "__main__":
    diagnostico = diagnostico_base_suja("pedidos_loja.csv")
    metricas = metricas_base_limpa("pedidos_limpos.csv")
    print(json.dumps(diagnostico, indent=2, ensure_ascii=False))
    print(json.dumps(metricas, indent=2, ensure_ascii=False))