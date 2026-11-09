
import os
import streamlit as st
api_key = st.secrets.get("GEMINI_API_KEY", "")
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 HealthGuard AI")
st.subheader("Your Smart Multilingual Health Information Assistant")

st.info(
    "HealthGuard AI provides general health education, not medical "
    "diagnosis or treatment. Always consult a qualified healthcare professional."
)

# Language selection
language = st.selectbox(
    "Choose your language",
    ["English", "తెలుగు (Telugu)", "हिन्दी (Hindi)"]
)

language_instructions = {
    "English": "Reply in simple English.",
    "తెలుగు (Telugu)": "సులభమైన తెలుగులో సమాధానం ఇవ్వండి.",
    "हिन्दी (Hindi)": "सरल हिंदी में जवाब दें।"
}

# API configuration
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask a general health question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not api_key:
            answer = (
                "AI connection is not configured. Please check your "
                "GEMINI_API_KEY in the .env file."
            )
            st.warning(answer)
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are HealthGuard AI, a safe health education assistant.

                {language_instructions[language]}

                Answer in clear, simple language.
                Explain general health information and sensible precautions.
                Do not diagnose diseases.
                Do not prescribe medicines, doses, or personalized treatments.
                Do not recommend unverified Ayurvedic remedies.
                Encourage the user to consult a qualified healthcare professional.
                If the user describes an emergency, advise contacting local
                emergency services immediately. In India, call 112.

                User question: {question}
                """

                with st.spinner("HealthGuard AI is preparing an answer..."):
                    response = client.interactions.create(
                        model=model,
                        input=prompt
                    )

                answer = getattr(response, "output_text", None)

                if not answer:
                    answer = str(response)

                st.markdown(answer)

            except Exception:
                answer = (
                    "The AI service is temporarily unavailable. "
                    "Please try again later. For urgent health concerns, "
                    "contact a healthcare professional or call 112 in India."
                )
                st.warning(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.divider()
st.caption(
    "HealthGuard AI | Health education only | "
    "Not a replacement for professional medical care"
)
