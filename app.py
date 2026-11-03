import streamlit as st
from pypdf import PdfReader
from ai_engine import ask_gemini

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Career Assistant")
st.write("Your personal AI assistant for career growth.")

chat_tab, resume_tab = st.tabs(["💬 AI Chatbot", "📄 Resume Analyzer"])

# ---------------- CHATBOT ----------------
with chat_tab:
    st.header("Ask your career questions")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask me anything about your career...")

    if user_question:
        st.session_state.messages.append(
            {"role": "user", "content": user_question}
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_gemini(user_question)
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


# ---------------- RESUME ANALYZER ----------------
with resume_tab:
    st.header("📄 AI Resume Analyzer")
    st.write("Upload your resume in PDF format to receive AI-powered feedback.")

    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        st.success("Resume uploaded successfully!")

        if st.button("Analyze My Resume"):
            try:
                pdf_reader = PdfReader(uploaded_file)

                resume_text = ""

                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        resume_text += page_text + "\n"

                if not resume_text.strip():
                    st.error(
                        "I couldn't read text from this PDF. "
                        "Please upload a text-based PDF rather than a scanned image."
                    )
                else:
                    prompt = f"""
                    You are an experienced resume reviewer and career advisor.

                    Analyze the following resume and give feedback in simple English.

                    Include these sections:

                    1. Resume Summary
                    2. Key Strengths
                    3. Weaknesses or Missing Information
                    4. Technical Skills Found
                    5. Skills the Candidate Could Improve
                    6. Suggestions to Improve the Resume
                    7. Suitable Entry-Level Job Roles

                    Be honest, practical, and supportive.
                    Do not invent qualifications or experience.

                    RESUME TEXT:
                    {resume_text[:20000]}
                    """

                    with st.spinner("AI is analyzing your resume..."):
                        result = ask_gemini(prompt)

                    st.subheader("Your Resume Analysis")
                    st.markdown(result)

            except Exception as e:
                st.error(f"Something went wrong while reading the PDF: {e}")