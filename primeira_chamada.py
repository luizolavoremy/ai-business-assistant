from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

resposta = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explique em duas frases o que é a taxa de cancelamento de pedidos de uma loja.",
)
print(resposta.text)