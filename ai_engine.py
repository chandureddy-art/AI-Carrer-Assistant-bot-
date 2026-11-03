import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def ask_gemini(question):

    if client is None:
        return "Error: Gemini API key not found."

    models = [
        "gemini-3.1-flash-lite"
    ]

    for model in models:

        try:
            print("Trying model:", model)

            response = client.models.generate_content(
                model=model,
                contents=question
            )

            return response.text

        except Exception as e:
            print("Model failed:", model)
            print("Error:", e)

            time.sleep(2)

    return "Both Gemini models are temporarily unavailable. Please try again."