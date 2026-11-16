from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

for modelo in client.models.list():
    if "flash" in modelo.name:
        print(modelo.name)