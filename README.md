# AI Business Assistant

Sistema de três agentes de IA que lê uma base de pedidos de loja online e gera um relatório com validação de qualidade, análise comercial e recomendações. Um comando, `python main.py`, roda tudo e salva o `relatorio.md`.

> **Sobre este projeto:** é um projeto de estudo, construído com apoio de IA (Claude). O código e os prompts foram desenvolvidos em conversa e refinados em várias versões, e cada versão foi testada e conferida contra números já conhecidos dos projetos anteriores. A base é **sintética**, gerada para estudo, e os números não representam nenhuma empresa real.

Faz parte de uma série com a mesma base: [análise com pandas](https://github.com/luizolavoremy/analise-pedidos-loja), [SQL](https://github.com/luizolavoremy/analise-pedidos-loja-sql) e [dashboard em Power BI](https://github.com/luizolavoremy/analise-pedidos-loja-powerbi). Veja um exemplo de saída em [`relatorio.md`](relatorio.md).

## Como funciona

1. O **pandas** calcula os números: o diagnóstico da base suja (`pedidos_loja.csv`) e as métricas da base limpa (`pedidos_limpos.csv`). A IA não faz conta.
2. O **Agente 1 (validação)** recebe o diagnóstico e lista os problemas de qualidade por gravidade. Ele só diagnostica e não altera dados.
3. O **Agente 2 (análise comercial)** recebe as métricas e escreve 7 achados, sempre citando números.
4. O **Agente 3 (recomendações)** recebe os textos dos dois primeiros e propõe ações, classificando cada uma como "os dados provam" ou "os dados só sugerem".
5. O **orquestrador** (`main.py`) chama os três em ordem, passa o resultado de um para o próximo e monta o relatório.
6. Uma **checagem automática** (`verificacao.py`) confere se cada número do texto existe nas métricas.

## Tecnologias

Python 3.14 · pandas · Google Gemini API (`google-genai`) · python-dotenv · Git/GitHub

A API usada tem camada gratuita, então o projeto roda sem custo. A chave é criada em [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

## Evolução dos prompts

Cada agente passou por várias versões. Os testes sempre compararam a saída com números conhecidos.

| Agente | Versões | O que cada ajuste corrigiu |
|---|---|---|
| Validação | 3 | Hesitação em recuperar estado e categoria vazios (o prompt agora explica que cada cidade tem um estado e cada produto uma categoria); problemas omitidos sem aviso (o limite de 10 itens cortou 2 dos 12 problemas); eco da instrução dentro da resposta |
| Análise comercial | 5 | Contraste inventado ("mas") sem mudança de posição; totais dos 24 meses lidos como se fossem de 2024; ranking errado; dígito trocado; campo citado no prompt que não existia nos dados |
| Recomendações | 3 | Ação de crescimento ausente; causa fora dos dados classificada como "os dados provam"; nomes técnicos de campo no texto |

## Problemas encontrados

- **Chave da API recusada (`401 ACCESS_TOKEN_TYPE_UNSUPPORTED`).** As chaves novas do AI Studio começam com `AQ.`. Um script de diagnóstico (`diagnostico_chave.py`) mostrou que o `.env` estava certo, e criar uma chave nova resolveu.
- **Modelo indisponível (`404`).** O modelo do primeiro teste não estava mais disponível para contas novas, e a mensagem de erro indicava o substituto. Um script (`teste_api.py`) lista os modelos que a chave enxerga.
- **Omissão silenciosa.** Um limite de tamanho no prompt ("até 10 itens") fez o agente cortar 2 problemas sem avisar. A correção foi pedir todos os itens e uma linha com o total, que permite conferir.
- **Ranking feito de cabeça.** O modelo errou posições de categorias e meses. A correção foi o pandas entregar as posições prontas (`posicao_unidades`, `posicao_receita`, `top3_meses`, `bottom3_meses`).
- **Campo inexistente.** O prompt citava um campo que ainda não estava no JSON, e o modelo ordenou por conta própria, sem erro nenhum.
- **Erro de dígito persistente.** O modelo escreveu R$ 947.832,37 no lugar de R$ 947.832,27 em três execuções, mesmo com uma regra de copiar exato. Prompt reduziu o erro, mas só o código garante, e por isso existe a checagem automática.
- **Número certo no assunto errado.** Em uma execução, a recomendação atribuiu à Beleza as 1.338 unidades do Esporte. Todos os números existiam nos dados, então a checagem não acusou nada. O relatório de exemplo foi gerado na 2ª execução.
- **Servidor ocupado (`503`).** O SDK repetiu a chamada sozinho e a execução seguiu.

## Limitações

- A checagem automática pega número inventado ou digitado errado, mas **não** pega número certo ligado ao assunto errado, e ignora os números de 0 a 12, o 24 e os anos. A revisão humana continua necessária.
- O resultado varia entre execuções: uma ação pode aparecer ou sumir, e o formato do texto muda (por exemplo, o rótulo "Classificação:" nem sempre sai).
- As métricas de receita incluem 20 pedidos com preço unitário negativo (−R$ 6.329,96, cerca de 0,3% da receita) que a limpeza dos projetos anteriores não tratou. A validação (Agente 1) sinaliza o problema nos dados brutos.
- A análise descreve o que os dados mostram, sem testar causas. As hipóteses das recomendações são marcadas como tal.
- A base é sintética.

## Como rodar

```bash
git clone https://github.com/luizolavoremy/ai-business-assistant.git
cd ai-business-assistant
python -m venv venv
venv\Scripts\activate        # Windows (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env       # Mac/Linux: cp .env.example .env
```

Abra o arquivo `.env` e coloque a sua chave no lugar de `cole_sua_chave_aqui`. O `.env` está no `.gitignore` e nunca vai para o GitHub. Depois:

```bash
python main.py
```

## Estrutura do repositório

```
ai-business-assistant/
├── main.py                 # orquestrador: roda os 3 agentes e gera o relatório
├── agentes.py              # prompts e chamadas ao modelo
├── analise.py              # diagnóstico e métricas, calculados em pandas
├── verificacao.py          # confere se os números do texto existem nas métricas
├── pedidos_loja.csv        # base original (suja)
├── pedidos_limpos.csv      # base limpa no projeto 1
├── relatorio.md            # exemplo de relatório gerado
├── primeira_chamada.py     # primeiro teste da API
├── teste_api.py            # lista os modelos disponíveis para a chave
├── diagnostico_chave.py    # diagnóstico do erro 401
├── .env.example            # modelo do arquivo de chave
├── requirements.txt
└── README.md
```

## Próximos passos

- Interface web para enviar o CSV.
- Deixar o modelo escolher as ferramentas, em vez de uma sequência fixa.
- Tratar os preços negativos nas métricas.

## Autor

Luiz Olavo Remy Firmino · https://www.linkedin.com/in/luiz-olavo-remy · luiz.olavo.remy@gmail.com
