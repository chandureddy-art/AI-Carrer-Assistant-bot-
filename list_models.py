from dotenv import load_dotenv
from google import genai
import os

print("Starting Gemini model check...")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)

        print("Connected! Checking available models...")

        models = client.models.list()

        for model in models:
            print("Model:", model.name)

        print("Model check completed.")

    except Exception as e:
        print("ERROR:", e)