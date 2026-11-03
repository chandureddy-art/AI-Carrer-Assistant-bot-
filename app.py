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


# ---------------- PDF READER ----------------

def extract_resume_text(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text + "\n"

    return resume_text


# ---------------- MAIN TABS ----------------

chat_tab, resume_tab, jobs_tab, interview_tab = st.tabs([
    "💬 AI Chatbot",
    "📄 Resume Analyzer",
    "💼 Job Recommendations",
    "🎯 Interview Preparation"
])


# ==================================================
# FEATURE 1: AI CHATBOT
# ==================================================

with chat_tab:

    st.header("AI Career Chatbot")

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

    st.header("AI Resume Analyzer")

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

                    Give these sections:

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

    st.header("AI Job Recommendations")

    st.write("Find suitable job roles based on your skills.")

    job_resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        key="job_resume"
    )

    skills = st.text_area(
        "Enter your skills",
        placeholder="Example: Python, Java, SQL, HTML"
    )

    qualification = st.text_input(
        "Your qualification",
        placeholder="Example: B.Tech in Electronics"
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

    if st.button("Find Suitable Jobs"):

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
                You are an expert career advisor.

                Recommend suitable fresher job roles.

                Qualification: {qualification}
                Skills: {skills}
                Experience: {experience}
                Location: {location}
                Work Preference: {work_preference}

                Resume:
                {resume_text[:15000]}

                Include:
                1. Top 5 suitable job roles.
                2. Why each role is suitable.
                3. Skills required for each role.
                4. Best role to start with.
                5. Skills to learn.
                6. Job search strategy.
                7. A 30-day preparation plan.

                Do not invent live job vacancies.
                Keep the recommendations realistic.
                """

                with st.spinner("Finding suitable career options..."):
                    recommendations = ask_gemini(prompt)

                st.subheader("Your Job Recommendations")
                st.markdown(recommendations)

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ==================================================
# FEATURE 4: INTERVIEW PREPARATION
# ==================================================

with interview_tab:

    st.header("AI Interview Preparation")

    st.write(
        "Practice interview questions and prepare for fresher jobs."
    )

    interview_mode = st.selectbox(
        "Choose your preparation mode",
        [
            "HR Interview Questions",
            "Technical Interview Questions",
            "Generate My Interview Answer",
            "Mock Interview Practice"
        ]
    )

    # -------- HR QUESTIONS --------

    if interview_mode == "HR Interview Questions":

        st.subheader("HR Interview Preparation")

        role = st.text_input(
            "Enter the job role",
            placeholder="Example: Python Developer Fresher"
        )

        if st.button("Generate HR Questions"):

            prompt = f"""
            You are an experienced HR interviewer.

            Generate 10 common HR interview questions
            for the role: {role or "Fresher"}.

            For every question provide:
            1. Interview question.
            2. Simple sample answer.
            3. One tip for answering.

            Use simple English.
            Do not invent personal details about the candidate.
            """

            with st.spinner("Preparing HR questions..."):
                result = ask_gemini(prompt)

            st.markdown(result)

    # -------- TECHNICAL QUESTIONS --------

    elif interview_mode == "Technical Interview Questions":

        st.subheader("Technical Interview Preparation")

        subject = st.selectbox(
            "Select your technical subject",
            [
                "Python",
                "Java",
                "SQL",
                "HTML and CSS",
                "Generative AI",
                "Machine Learning",
                "Computer Networks",
                "Electronics"
            ]
        )

        level = st.selectbox(
            "Select difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        if st.button("Generate Technical Questions"):

            prompt = f"""
            Act as a technical interviewer.

            Generate 10 {level} level interview questions
            about {subject} for a fresher.

            Provide:
            1. Question.
            2. Correct answer.
            3. Simple explanation.
            4. Practical example when useful.

            Use simple English.
            """

            with st.spinner("Generating technical questions..."):
                result = ask_gemini(prompt)

            st.markdown(result)

    # -------- ANSWER GENERATOR --------

    elif interview_mode == "Generate My Interview Answer":

        st.subheader("AI Interview Answer Generator")

        question = st.text_area(
            "Enter the interview question",
            placeholder="Example: Tell me about yourself."
        )

        candidate_details = st.text_area(
            "Enter your actual background and skills",
            placeholder="Example: I am a B.Tech fresher. I know beginner Python and Java."
        )

        if st.button("Generate My Answer"):

            if not question.strip():
                st.warning("Please enter an interview question.")

            else:

                prompt = f"""
                You are an interview coach.

                Prepare a natural and professional sample answer
                for this interview question:

                QUESTION:
                {question}

                CANDIDATE DETAILS:
                {candidate_details}

                Instructions:
                1. Use simple spoken English.
                2. Keep the answer natural.
                3. Make it suitable for a fresher when applicable.
                4. Do not invent experience, projects or qualifications.
                5. Give a short version the candidate can practice.
                """

                with st.spinner("Preparing your answer..."):
                    result = ask_gemini(prompt)

                st.markdown(result)

    # -------- MOCK INTERVIEW --------

    elif interview_mode == "Mock Interview Practice":

        st.subheader("Practice a Mock Interview")

        mock_role = st.text_input(
            "Enter the job role for your mock interview",
            placeholder="Example: Generative AI Engineer Fresher",
            key="mock_role"
        )

        if "mock_question" not in st.session_state:
            st.session_state.mock_question = ""

        if st.button("Start Mock Interview"):

            prompt = f"""
            Act as a friendly but professional interviewer.

            Start a mock interview for:
            {mock_role or "Fresher Job"}

            Ask only ONE interview question.
            Do not provide the answer.
            Keep it suitable for a fresher.
            """

            with st.spinner("Preparing your interview question..."):
                st.session_state.mock_question = ask_gemini(prompt)

        if st.session_state.mock_question:

            st.info(st.session_state.mock_question)

            mock_answer = st.text_area(
                "Type your answer here",
                key="mock_answer"
            )

            if st.button("Evaluate My Answer"):

                if not mock_answer.strip():

                    st.warning("Please write your answer first.")

                else:

                    feedback_prompt = f"""
                    You are an experienced interview coach.

                    Interview question:
                    {st.session_state.mock_question}

                    Candidate answer:
                    {mock_answer}

                    Evaluate the answer.

                    Give:
                    1. What was good.
                    2. What needs improvement.
                    3. Clarity and communication feedback.
                    4. A better sample answer.
                    5. Three practical tips.

                    Be encouraging and honest.
                    Use simple English.
                    """

                    with st.spinner("Evaluating your answer..."):
                        feedback = ask_gemini(feedback_prompt)

                    st.subheader("Your Interview Feedback")
                    st.markdown(feedback)