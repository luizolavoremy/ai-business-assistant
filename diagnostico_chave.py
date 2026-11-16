import os
from dotenv import load_dotenv

load_dotenv()
chave = os.environ.get("GEMINI_API_KEY", "")

print("Chave encontrada:", chave != "")
print("Tamanho:", len(chave))
print("Começa com AQ.:", chave.startswith("AQ."))
print("Tem espaço ou aspas:", chave != chave.strip() or '"' in chave or "'" in chave)
print("GOOGLE_API_KEY também definida:", "GOOGLE_API_KEY" in os.environ)