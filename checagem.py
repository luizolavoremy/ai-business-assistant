import re

from analise import diagnostico_base_suja, metricas_base_limpa

# contagens e anos que aparecem no texto sem vir do JSON
IGNORAR = {"1", "2", "3", "4", "5", "6", "7", "24", "2023", "2024"}

PADRAO_NUMERO = re.compile(r"(?<![\d.,])\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")


def _br(valor, casas):
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _numeros_permitidos(dados):
    permitidos = set()

    def percorrer(item):
        if isinstance(item, dict):
            for v in item.values():
                percorrer(v)
        elif isinstance(item, bool):
            return
        elif isinstance(item, int):
            permitidos.add(_br(item, 0))
        elif isinstance(item, float):
            permitidos.add(_br(item, 2))
            if item == int(item):
                permitidos.add(_br(item, 0))

    percorrer(dados)
    return permitidos


def _numeros_do_texto(texto):
    texto = re.sub(r"(?m)^\s*\d+\.\s", "", texto)         # numeração de lista
    texto = re.sub(r"\b\d{4}-\d{2}\b", "", texto)         # meses como 2024-11
    texto = re.sub(r"Total de problemas listados: \d+", "", texto)
    texto = re.sub(r"\d{2}/\d{2}/\d{4}", "", texto)       # datas
    return PADRAO_NUMERO.findall(texto)


def _conferir(texto, permitidos, secao):
    erros = []
    for numero in _numeros_do_texto(texto):
        if numero not in IGNORAR and numero not in permitidos:
            erros.append(f"[{secao}] número não encontrado no JSON: {numero}")
    return erros


def _conferir_variacoes(texto, diagnostico):
    erros = []
    blocos = re.split(r"\n\s*\n", texto)
    for coluna in ("cidade", "categoria", "status"):
        v = diagnostico[f"variacoes_{coluna}"]
        esperado = (
            f"{v['valores_distintos']} valores distintos, "
            f"{v['valores_apos_padronizar']} após padronizar"
        )
        candidatos = [b for b in blocos if "variaç" in b.lower() and coluna in b.lower()]
        if not any(esperado in b for b in candidatos):
            erros.append(f"[validação] variações de {coluna}: esperado '{esperado}'")
    return erros


def _conferir_acoes_validacao(texto):
    esperado = [
        ("preço unitário negativo", "Separar"),
        ("quantidade zero", "Separar"),
        ("preço unitário nulo", "Separar"),
        ("duplicada", "Remover"),
        ("frete", "Converter"),
        ("datas", "Padronizar"),
        ("variações", "Padronizar"),
        ("estado nulo", "Recuperar"),
        ("categoria nula", "Recuperar"),
        ("cidade nula", "Recuperar"),
    ]
    erros = []
    for bloco in re.split(r"\n\s*\n", texto):
        problema = re.search(r"Problema:\s*(.+)", bloco)
        acao = re.search(r"Ação[^:\n]*:\s*(.+)", bloco)
        if not problema or not acao:
            continue
        nome = problema.group(1).lower()
        for chave, verbo in esperado:
            if chave in nome:
                if not acao.group(1).strip().startswith(verbo):
                    erros.append(
                        f"[validação] '{problema.group(1).strip()}' deveria ter ação '{verbo}...'"
                    )
                break
    return erros


def _conferir_frases_proibidas(conteudo):
    proibidas = ["24 anos"]
    return [f"[geral] frase incorreta: {f}" for f in proibidas if f in conteudo]


def _conferir_ticket_estados(texto, metricas):
    erros = []
    for valor, uf in re.findall(r"R\$ ([\d.,]+) em ([A-Z]{2})\b", texto):
        real = metricas["por_estado"].get(uf)
        if real is None or _br(real["ticket_medio"], 2) != valor:
            erros.append(f"[análise] ticket médio de {uf} não confere: R$ {valor}")
    return erros


def _conferir_intervalo_estados(texto, metricas):
    erros = []
    tickets = [v["ticket_medio"] for v in metricas["por_estado"].values()]
    menor, maior = _br(min(tickets), 2), _br(max(tickets), 2)
    for trecho in re.findall(r"ticket médio[^.]*\.", texto):
        if "variando" in trecho:
            if "marketplace" in trecho.lower() or "canais" in trecho.lower():
                erros.append("[análise] intervalo de ticket por estado cita canais")
            elif menor not in trecho or maior not in trecho:
                erros.append(
                    f"[análise] intervalo de ticket por estado deveria ser R$ {menor} a R$ {maior}"
                )
    return erros


def _conferir_verbos(texto):
    erros = []
    for linha in texto.splitlines():
        if re.match(r"\s*\d+\.\s*Invista\b", linha):
            erros.append("[recomendações] ação começa com 'Invista': use 'Mantenha' ou 'Investigue'")
    return erros


def _conferir_categorias_repetidas(texto, metricas):
    erros = []
    acoes = re.findall(r"(?m)^\s*\d+\.\s*(.+)$", texto)
    for categoria in metricas["por_categoria"]:
        n = sum(1 for a in acoes if categoria in a)
        if n > 1:
            erros.append(f"[recomendações] {n} ações falam de {categoria}")
    return erros


def checar_relatorio(caminho_relatorio, diagnostico, metricas):
    with open(caminho_relatorio, encoding="utf-8") as f:
        conteudo = f.read()
    partes = re.split(r"(?m)^## ", conteudo)
    # partes[0] = cabeçalho; 1 = validação; 2 = análise; 3 = recomendações
    do_diagnostico = _numeros_permitidos(diagnostico)
    de_tudo = do_diagnostico | _numeros_permitidos(metricas)

    erros = []
    erros += _conferir(partes[1], do_diagnostico, "validação")
    erros += _conferir(partes[2], de_tudo, "análise")
    erros += _conferir(partes[3], de_tudo, "recomendações")
    erros += _conferir_variacoes(partes[1], diagnostico)
    erros += _conferir_acoes_validacao(partes[1])
    erros += _conferir_ticket_estados(partes[2], metricas)
    erros += _conferir_intervalo_estados(partes[2], metricas)
    erros += _conferir_verbos(partes[3])
    erros += _conferir_categorias_repetidas(partes[3], metricas)
    erros += _conferir_frases_proibidas(conteudo)
    return erros


if __name__ == "__main__":
    diag = diagnostico_base_suja("pedidos_loja.csv")
    met = metricas_base_limpa("pedidos_limpos.csv")
    erros = checar_relatorio("relatorio.md", diag, met)
    print("\n".join(erros) if erros else "Todos os números conferem com o JSON.")