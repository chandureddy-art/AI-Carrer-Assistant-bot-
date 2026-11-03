import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


def ask_gemini(question):

    if client is None:
        return "Error: Gemini API key not found. Check your .env file."

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=question
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"