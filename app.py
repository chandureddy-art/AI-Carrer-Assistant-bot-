import streamlit as st
from pypdf import PdfReader
from ai_engine import ask_gemini


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Career Assistant")
st.write("Your personal AI assistant for career growth.")


# ---------------- PDF READER FUNCTION ----------------

def extract_resume_text(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text + "\n"

    return resume_text


# ---------------- THREE FEATURES ----------------

chat_tab, resume_tab, jobs_tab = st.tabs([
    "💬 AI Chatbot",
    "📄 Resume Analyzer",
    "💼 Job Recommendations"
])


# ==================================================
# FEATURE 1: AI CHATBOT
# ==================================================

with chat_tab:

    st.header("💬 AI Career Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask me anything about your career..."
    )

    if user_question:

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):
                answer = ask_gemini(user_question)

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


# ==================================================
# FEATURE 2: RESUME ANALYZER
# ==================================================

with resume_tab:

    st.header("📄 AI Resume Analyzer")

    st.write("Upload your resume in PDF format.")

    resume_file = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        key="analyzer_resume"
    )

    if resume_file:

        st.success("Resume uploaded successfully!")

        if st.button("Analyze My Resume"):

            try:
                resume_text = extract_resume_text(resume_file)

                if not resume_text.strip():

                    st.error("No readable text found in this PDF.")

                else:

                    prompt = f"""
                    You are an experienced resume reviewer.

                    Analyze this resume in simple English.

                    Give the following sections:

                    1. Resume Summary
                    2. Key Strengths
                    3. Weaknesses
                    4. Technical Skills
                    5. Skills to Improve
                    6. Resume Improvement Suggestions
                    7. Suitable Fresher Job Roles

                    Do not invent qualifications or experience.

                    RESUME:
                    {resume_text[:20000]}
                    """

                    with st.spinner("Analyzing your resume..."):
                        result = ask_gemini(prompt)

                    st.subheader("Your Resume Analysis")
                    st.markdown(result)

            except Exception as e:
                st.error(f"Error reading resume: {e}")


# ==================================================
# FEATURE 3: JOB RECOMMENDATIONS
# ==================================================

with jobs_tab:

    st.header("💼 AI Job Recommendations")

    st.write(
        "Find suitable job roles based on your resume, "
        "skills, location, and work preferences."
    )

    st.info(
        "Upload your resume or enter your skills manually. "
        "You can also provide both."
    )

    job_resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        key="job_resume"
    )

    skills = st.text_area(
        "Enter your skills",
        placeholder="Example: Python, Java, SQL, HTML, Communication"
    )

    qualification = st.text_input(
        "Your qualification",
        placeholder="Example: B.Tech in Electronics and Communication"
    )

    experience = st.selectbox(
        "Your experience level",
        [
            "Fresher",
            "Less than 1 year",
            "1-2 years",
            "More than 2 years"
        ]
    )

    location = st.text_input(
        "Preferred job location",
        value="India"
    )

    work_preference = st.selectbox(
        "Preferred work type",
        [
            "Office job",
            "Work from home",
            "Hybrid",
            "Field work",
            "Any work type"
        ]
    )

    if st.button("Find Suitable Jobs", type="primary"):

        try:
            resume_text = ""

            if job_resume is not None:
                resume_text = extract_resume_text(job_resume)

            if not resume_text.strip() and not skills.strip():
                st.warning(
                    "Please upload your resume or enter your skills."
                )

            else:

                prompt = f"""
                You are an expert career advisor who helps job seekers
                find suitable entry-level career opportunities in India.

                Based on the candidate details below, recommend
                suitable job roles.

                CANDIDATE DETAILS:

                Qualification: {qualification}
                Skills: {skills}
                Experience: {experience}
                Preferred Location: {location}
                Work Preference: {work_preference}

                RESUME CONTENT:
                {resume_text[:15000]}

                Give your answer in simple English using these sections:

                1. TOP 5 SUITABLE JOB ROLES
                For each role explain:
                - Job title
                - Why it suits the candidate
                - Important skills required
                - Skills the candidate should improve

                2. BEST ROLE TO START WITH
                Explain which role is the best starting point
                and why.

                3. SKILLS TO LEARN
                Give a practical list of skills to improve
                job opportunities.

                4. JOB SEARCH STRATEGY
                Explain how this candidate can search and apply
                for jobs in the preferred location.

                5. 30-DAY PREPARATION PLAN
                Give a simple weekly plan to prepare for interviews
                and fresher job applications.

                IMPORTANT:
                - Do not invent job vacancies or company openings.
                - These are career recommendations, not verified
                  live job listings.
                - Consider the candidate's experience level.
                - Keep the advice realistic for a fresher.
                """

                with st.spinner(
                    "AI is finding suitable career options..."
                ):
                    recommendations = ask_gemini(prompt)

                st.subheader("Your Personalized Job Recommendations")
                st.markdown(recommendations)

        except Exception as e:
            st.error(f"Something went wrong: {e}")