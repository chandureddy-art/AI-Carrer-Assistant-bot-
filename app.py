import streamlit as st
from ai_engine import ask_gemini

# Page configuration
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide"
)

# Application heading
st.title("🚀 AI Career Assistant")
st.subheader("Your Personal AI Career Guide")

st.write(
    "Get help with resumes, interviews, skills, "
    "career paths and job preparation."
)

# Sidebar
with st.sidebar:
    st.title("Career Assistant")
    st.write("Powered by Gemini AI")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.info(
        "Welcome! Ask me anything about your career."
    )

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_question = st.chat_input(
    "Ask your career-related question..."
)

if user_question:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):
            response = ask_gemini(user_question)

        st.markdown(response)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })