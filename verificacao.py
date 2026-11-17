import re

NUMEROS_ESTRUTURAIS = set(range(0, 13)) | {24, 2023, 2024}


def _numeros_do_json(dados):
    encontrados = set()
    if isinstance(dados, dict):
        for valor in dados.values():
            encontrados |= _numeros_do_json(valor)
    elif isinstance(dados, (int, float)) and not isinstance(dados, bool):
        encontrados.add(round(float(dados), 2))
    return encontrados


def numeros_sem_origem(texto, dados):
    permitidos = _numeros_do_json(dados) | NUMEROS_ESTRUTURAIS
    texto = re.sub(r"\d{4}-\d{2}", "", texto)
    texto = re.sub(r"(?m)^\s*\d+\.\s", "", texto)
    suspeitos = []
    for bruto in re.findall(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", texto):
        valor = round(float(bruto.replace(".", "").replace(",", ".")), 2)
        if valor not in permitidos:
            suspeitos.append(bruto)
    return suspeitos