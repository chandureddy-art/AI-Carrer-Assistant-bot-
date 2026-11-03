import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API KEY NOT FOUND")
else:
    client = genai.Client(api_key=api_key)

    try:
        print("Connecting to Gemini...")

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents="Say hello in one sentence."
        )

        print("SUCCESS!")
        print(response.text)

    except Exception as e:
        print("FAILED!")
        print(type(e).__name__)
        print(e)