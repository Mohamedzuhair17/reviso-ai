import io
import os
import time
import streamlit as st
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted, PermissionDenied

# ================= ENV =================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY missing. Add it to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ================= PAGE =================
st.set_page_config(
    page_title="Reviso — AI School Assistant",
    layout="wide"
)

# ================= SAFE GENERATE =================
def safe_generate(prompt, retries=2):
    for _ in range(retries):
        try:
            return model.generate_content(prompt).text
        except ResourceExhausted:
            time.sleep(5)
        except PermissionDenied:
            return "❌ Permission denied. Check API & billing."
    return "⚠️ AI busy. Try again later."

# ================= SESSION =================
for key in ["mode", "output", "chat", "last_run"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat" else []

# ================= UI =================
st.title("Reviso")
st.caption("Understand • Revise • Ask")

uploaded = st.file_uploader("Upload study notes (PDF)", type=["pdf"])

if uploaded:
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
    notes = " ".join(p.extract_text() or "" for p in reader.pages)

    if not notes.strip():
        st.error("No readable text found.")
        st.stop()

    left, right = st.columns([3, 1])

    # ================= LEFT PANEL =================
    with left:
        b1, b2 = st.columns(2)

        with b1:
            if st.button("🧠 Understand", use_container_width=True):
                st.session_state.mode = "summary"
                st.session_state.output = None
                st.session_state.chat = []

        with b2:
            if st.button("📄 Revise", use_container_width=True):
                st.session_state.mode = "cheat"
                st.session_state.output = None
                st.session_state.chat = []

        # Cooldown
        if st.session_state.last_run:
            if time.time() - st.session_state.last_run < 8:
                st.warning("Please wait a few seconds...")
                st.stop()

        if st.session_state.mode == "summary" and st.session_state.output is None:
            st.session_state.last_run = time.time()
            with st.spinner("Generating explanation..."):
                st.session_state.output = safe_generate(
                    f"""
                    Create a deep, exam-oriented explanation.
                    Use headings, definitions, and examples.

                    NOTES:
                    {notes[:6000]}
                    """
                )

        if st.session_state.mode == "cheat" and st.session_state.output is None:
            st.session_state.last_run = time.time()
            with st.spinner("Creating cheat sheet..."):
                st.session_state.output = safe_generate(
                    f"""
                    Create a ONE-PAGE exam cheat sheet.
                    Bullet points only.

                    NOTES:
                    {notes[:6000]}
                    """
                )

        if st.session_state.output:
            st.markdown("### Output")
            st.write(st.session_state.output)

    # ================= RIGHT SIDEBAR CHATBOT =================
    with right:
        st.markdown("### 🤖 Questioning Chatbot")

        if st.session_state.output and st.session_state.mode in ["summary", "cheat"]:
            q = st.text_input(
                "Ask from this content",
                placeholder="Ask a doubt...",
                key="qa_input"
            )

            if st.button("Ask", use_container_width=True) and q.strip():
                with st.spinner("Thinking..."):
                    ans = safe_generate(
                        f"""
                        Answer ONLY using the content below.

                        NOTES:
                        {notes[:6000]}

                        GENERATED CONTENT:
                        {st.session_state.output[:6000]}

                        QUESTION:
                        {q}
                        """
                    )
                st.session_state.chat.append((q, ans))

            if st.session_state.chat:
                st.markdown("---")
                for ques, ans in reversed(st.session_state.chat):
                    st.markdown(f"**You:** {ques}")
                    st.markdown(
                        f"<div style='color:#cfd3ff'>{ans}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")

        else:
            st.info("Generate output to unlock chatbot")

else:
    st.info("Upload a PDF to begin.")
