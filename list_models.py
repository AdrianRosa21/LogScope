import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LLM_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    print("Modelos disponibles:")
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Error:", e)
