import io
import streamlit as st
import PyPDF2
import google.generativeai as genai
from pptx import Presentation

# ================= CONFIG =================
st.set_page_config(
    page_title="Reviso — The AI School Assistant",
    layout="wide"
)

# Get API key from Streamlit secrets
API_KEY = st.secrets["gemini_api_key"]
genai.configure(api_key=API_KEY)

def get_model():
    # Directly use a known supported model
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()
if model is None:
    st.error("No supported model found.")
    st.stop()

# ================= SESSION =================
if "mode" not in st.session_state:
    st.session_state.mode = None
if "output" not in st.session_state:
    st.session_state.output = None
if "ppt" not in st.session_state:
    st.session_state.ppt = None
if "notes" not in st.session_state:
    st.session_state.notes = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= LUXURY UI + ANIMATIONS =================
st.markdown(
    """
    <style>
    :root {
        --bg:#0b0c10;
        --panel:#111217;
        --soft:#151821;
        --border:rgba(255,255,255,.06);
        --text:#e7e9ee;
        --muted:#9aa0a6;
        --accent:#7c7cff;
    }

    html, body {
        background:var(--bg);
        color:var(--text);
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    header, footer, #MainMenu { display:none; }

    section[data-testid="stSidebar"] {
        background:var(--panel);
        border-right:1px solid var(--border);
        animation: slideIn 0.7s ease-out;
    }

    .block-container {
        max-width:1200px;
        padding:3.5rem 0;
    }

    .brand {
        font-size:3rem;
        font-weight:700;
        letter-spacing:-0.045em;
        animation: fadeUp 0.8s ease-out both;
    }

    .tagline {
        color:var(--muted);
        margin-bottom:3.2rem;
        animation: fadeUp 0.8s ease-out both;
    }

    button {
        background:var(--soft) !important;
        border:1px solid var(--border) !important;
        color:var(--text) !important;
        border-radius:16px !important;
        height:68px !important;
        font-size:1.05rem !important;
    }

    .divider {
        display:flex;
        align-items:center;
        margin:3.5rem 0;
        color:var(--muted);
        font-size:.75rem;
        letter-spacing:.18em;
    }

    .divider::before, .divider::after {
        content:"";
        flex:1;
        height:1px;
        background:var(--border);
    }

    .divider span { padding:0 1.3rem; }

    .content {
        font-size:1.05rem;
        line-height:2;
    }

    .info {
        background:var(--soft);
        border-radius:18px;
        padding:26px;
        border:1px solid var(--border);
        color:var(--muted);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### Reviso")
    st.markdown("The AI School Assistant")
    st.markdown("---")
    uploaded = st.file_uploader("Upload notes (PDF)", type=["pdf"])
    st.markdown("---")
    st.markdown("<small style='color:#9aa0a6;'>Private • Academic • Safe</small>", unsafe_allow_html=True)

# ================= MAIN =================
left, center, right = st.columns([1, 3, 1.2])

with center:
    st.markdown("<div class='brand'>Reviso</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>From notes to understanding.</div>", unsafe_allow_html=True)

    if uploaded:
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
        notes = " ".join(page.extract_text() or "" for page in reader.pages)

        if not notes.strip():
            st.error("No readable text found.")
            st.stop()

        st.session_state.notes = notes

        st.markdown("### Choose how you want to study")
        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🧠 Understand", use_container_width=True):
                st.session_state.mode = "summary"
                st.session_state.output = None
                st.session_state.chat_history = []

        with c2:
            if st.button("📄 Revise", use_container_width=True):
                st.session_state.mode = "cheat"
                st.session_state.output = None
                st.session_state.chat_history = []

        with c3:
            if st.button("📊 Present", use_container_width=True):
                st.session_state.mode = "ppt"
                st.session_state.output = None

        if st.session_state.mode == "summary" and st.session_state.output is None:
            with st.spinner("Reviso is explaining your notes..."):
                st.session_state.output = model.generate_content(
                    f"Create a deep, exam-oriented explanation:\n\n{notes[:15000]}"
                ).text

        if st.session_state.mode == "cheat" and st.session_state.output is None:
            with st.spinner("Reviso is preparing a revision sheet..."):
                st.session_state.output = model.generate_content(
                    f"Create a ONE-PAGE exam cheat sheet:\n\n{notes[:15000]}"
                ).text

        if st.session_state.output:
            st.markdown("<div class='divider'><span>OUTPUT</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content'>{st.session_state.output}</div>", unsafe_allow_html=True)

    else:
        st.info("Upload your notes to begin.")

# ================= RIGHT PANEL — QUESTIONING CHATBOT =================
with right:
    if st.session_state.output is None:
        st.markdown(
            """
            <div class="info">
            <b>Questioning Chatbot</b><br><br>
            Complete <b>Understand</b> or <b>Revise</b>
            to unlock questioning mode.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("### 🧪 Questioning Chatbot")

        q = st.text_input("Ask a doubt / request questions")

        if st.button("Ask"):
            if q.strip():
                prompt = f"""
You are a questioning tutor.
Use the notes and output to answer clearly and academically.

NOTES:
{st.session_state.notes[:8000]}

OUTPUT:
{st.session_state.output[:8000]}

QUESTION:
{q}
"""
                ans = model.generate_content(prompt).text
                st.session_state.chat_history.append(("You", q))
                st.session_state.chat_history.append(("Reviso", ans))

        for role, msg in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🤖 Reviso:** {msg}")
