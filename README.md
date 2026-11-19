AI Business Assistant

Sistema de três agentes de IA que lê uma base de pedidos de loja online e gera um relatório com validação de qualidade, análise comercial e recomendações. Tem dois orquestradores: a v1 (main.py), que chama os agentes numa sequência fixa, e a v2 (orquestrador_v2.py), em que o próprio modelo escolhe quais ferramentas chamar e refaz uma etapa quando a checagem de números acusa erro.

Sobre este projeto: é um projeto de estudo, construído com apoio de IA (Claude). O código e os prompts foram desenvolvidos em conversa e refinados em várias versões, e cada versão foi testada e conferida contra números já conhecidos dos projetos anteriores. A base é sintética, gerada para estudo, e os números não representam nenhuma empresa real.

Faz parte de uma série com a mesma base: análise com pandas, SQL e dashboard em Power BI. Exemplos de saída: relatorio.md (v1) e relatorio_v2.md (v2).

Como funciona
O pandas calcula os números: o diagnóstico da base suja (pedidos_loja.csv) e as métricas da base limpa (pedidos_limpos.csv). A IA não faz conta.
O Agente 1 (validação) recebe o diagnóstico e lista os problemas de qualidade por gravidade. Ele só diagnostica e não altera dados.
O Agente 2 (análise comercial) recebe as métricas e escreve 7 achados, sempre citando números.
O Agente 3 (recomendações) recebe os textos dos dois primeiros e propõe ações, classificando cada uma como "os dados provam" ou "os dados só sugerem".
Uma checagem automática (verificacao.py) confere se cada número do texto existe nas métricas.
Uma padronização de formato por código (padronizar_formato, em agentes.py) completa as casas decimais, como R$ 216,20 e 6,70%.
Orquestrador v1 e v2
	v1 (main.py)	v2 (orquestrador_v2.py)
Quem conduz	O código, em sequência fixa	O modelo, com 4 ferramentas: validar_base, analisar_metricas, gerar_recomendacoes e verificar_numeros
Número sem origem na checagem	Só avisa no relatório	O modelo refaz a etapa afetada, até 2 vezes
Texto do relatório	Saída direta dos agentes	Vem dos resultados guardados pelas ferramentas, e não do texto final do modelo
Verificação final	Feita pelo código	Refeita pelo código, sem aceitar só a palavra do modelo
Registro	Não tem	O relatório lista a sequência de ferramentas que o modelo chamou
Custo	3 chamadas ao modelo	Mais chamadas e mais lento, o que pesa no plano gratuito

Na v2, as regras da instrução fixam quase toda a ordem, então o que o modelo decide de fato é a sequência e quando refazer uma etapa. No relatório de exemplo, ele fez as 4 chamadas na ordem esperada e não precisou refazer nada. O caminho de refação foi testado apenas com um modelo simulado, e ainda não com o modelo real.

Tecnologias

Python 3.14 · pandas · Google Gemini API (google-genai, com chamada automática de funções) · python-dotenv · Git/GitHub

A API usada tem camada gratuita, então o projeto roda sem custo. A chave é criada em aistudio.google.com/apikey.

Evolução dos prompts

Cada agente passou por várias versões. Os testes sempre compararam a saída com números conhecidos.

Agente	Versões	O que cada ajuste corrigiu
Validação	3	Hesitação em recuperar estado e categoria vazios (o prompt agora explica que cada cidade tem um estado e cada produto uma categoria); problemas omitidos sem aviso (o limite de 10 itens cortou 2 dos 12 problemas); eco da instrução dentro da resposta
Análise comercial	6	Contraste inventado ("mas") sem mudança de posição; totais dos 24 meses lidos como se fossem de 2024; ranking errado; dígito trocado; campo citado no prompt que não existia nos dados; limitação inventada ("apenas os dez principais estados")
Recomendações	4	Ação de crescimento ausente; causa fora dos dados classificada como "os dados provam"; nomes técnicos de campo no texto; classificação colada na linha de limitações
Problemas encontrados
Chave da API recusada (401 ACCESS_TOKEN_TYPE_UNSUPPORTED). As chaves novas do AI Studio começam com AQ.. Um script de diagnóstico (diagnostico_chave.py) mostrou que o .env estava certo, e criar uma chave nova resolveu.
Modelo indisponível (404). O modelo do primeiro teste não estava mais disponível para contas novas, e a mensagem de erro indicava o substituto. Um script (teste_api.py) lista os modelos que a chave enxerga.
Omissão silenciosa. Um limite de tamanho no prompt ("até 10 itens") fez o agente cortar 2 problemas sem avisar. A correção foi pedir todos os itens e uma linha com o total, que permite conferir.
Ranking feito de cabeça. O modelo errou posições de categorias e meses. A correção foi o pandas entregar as posições prontas (posicao_unidades, posicao_receita, top3_meses, bottom3_meses).
Campo inexistente. O prompt citava um campo que ainda não estava no JSON, e o modelo ordenou por conta própria, sem erro nenhum.
Erro de dígito persistente. O modelo escreveu R$ 947.832,37 no lugar de R$ 947.832,27 em três execuções, mesmo com uma regra de copiar exato. Prompt reduziu o erro, mas só o código garante, e por isso existe a checagem automática.
Número certo no assunto errado. Em uma execução, a recomendação atribuiu à Beleza as 1.338 unidades do Esporte. Todos os números existiam nos dados, então a checagem não acusou nada.
Limitação inventada. A análise disse que os dados "cobrem apenas os dez principais estados". Os 10 estados são todos os da base, e a soma das unidades deles é o total (9.665). O erro passou para as recomendações, onde ganhou uma classificação "os dados provam". A checagem de números não pega isso, porque não há número errado. A correção foi uma regra explícita no prompt.
Casas decimais perdidas. Valores como "R$ 385.033,1" e "6,7%" apareciam em algumas execuções e em outras não. Em vez de depender do prompt, a correção foi por código, em padronizar_formato.
Aviso do SDK. O SDK avisa que a chamada automática de funções direto em generate_content não é a forma recomendada (ele sugere o uso por chat). A v2 funcionou assim e o aviso foi mantido. A v2 usa um client separado do dos agentes, por causa de um problema reportado no SDK em que a configuração de ferramentas pode persistir entre chamadas do mesmo client.
Servidor ocupado (503). O SDK repetiu a chamada sozinho e a execução seguiu.
Limitações
A checagem automática pega número inventado ou digitado errado, mas não pega número certo ligado ao assunto errado, nem afirmação inventada sem número. Ela ignora os números de 0 a 12, o 24 e os anos. A revisão humana continua necessária.
O resultado varia entre execuções: uma ação pode aparecer ou sumir, e o formato do texto muda. Os achados da análise às vezes repetem a descrição do formato pedido no prompt, e as hipóteses das recomendações às vezes saem mais curtas.
A refação automática da v2 só foi testada com um modelo simulado.
As métricas de receita incluem 20 pedidos com preço unitário negativo (−R$ 6.329,96, cerca de 0,3% da receita) que a limpeza dos projetos anteriores não tratou. A validação (Agente 1) sinaliza o problema nos dados brutos.
A análise descreve o que os dados mostram, sem testar causas. As hipóteses das recomendações são marcadas como tal.
A base é sintética.
Como rodar
bash
git clone https://github.com/luizolavoremy/ai-business-assistant.git
cd ai-business-assistant
python -m venv venv
venv\Scripts\activate        # Windows (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env       # Mac/Linux: cp .env.example .env

Abra o arquivo .env e coloque a sua chave no lugar de cole_sua_chave_aqui. O .env está no .gitignore e nunca vai para o GitHub. Depois, escolha o orquestrador:

bash
python main.py                # v1: sequência fixa, gera relatorio.md
python orquestrador_v2.py     # v2: o modelo escolhe as ferramentas, gera relatorio_v2.md
Estrutura do repositório
ai-business-assistant/
├── main.py                 # orquestrador v1: sequência fixa
├── orquestrador_v2.py      # orquestrador v2: o modelo escolhe as ferramentas
├── agentes.py              # prompts, chamadas ao modelo e padronização de formato
├── analise.py              # diagnóstico e métricas, calculados em pandas
├── verificacao.py          # confere se os números do texto existem nas métricas
├── pedidos_loja.csv        # base original (suja)
├── pedidos_limpos.csv      # base limpa no projeto 1
├── relatorio.md            # exemplo de relatório da v1
├── relatorio_v2.md         # exemplo de relatório da v2
├── primeira_chamada.py     # primeiro teste da API
├── teste_api.py            # lista os modelos disponíveis para a chave
├── diagnostico_chave.py    # diagnóstico do erro 401
├── teste_formato.py        # teste da padronização de casas decimais
├── .env.example            # modelo do arquivo de chave
├── requirements.txt
└── README.md
Próximos passos
Testar a refação da v2 com o modelo real, forçando um número errado.
Interface web para enviar o CSV.
Tratar os preços negativos nas métricas.

## Autor

Luiz Olavo Remy Firmino · https://www.linkedin.com/in/luiz-olavo-remy · luiz.olavo.remy@gmail.com
