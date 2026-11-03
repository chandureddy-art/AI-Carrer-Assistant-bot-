import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


def ask_gemini(question):
    if client is None:
        return "Error: Gemini API key not found."

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=question
        )
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"