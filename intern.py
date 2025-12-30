import io
import os
import streamlit as st
import PyPDF2
import google.generativeai as genai
from pptx import Presentation
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found. Check .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# ================= CONFIG =================
st.set_page_config(
    page_title="Reviso — The AI School Assistant",
    layout="wide"
)

def get_model():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

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
        -webkit-font-smoothing: antialiased;
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
        animation: fadeUp 1s ease-out both;
    }

    button {
        background:var(--soft) !important;
        border:1px solid var(--border) !important;
        color:var(--text) !important;
        border-radius:16px !important;
        height:68px !important;
        font-size:1.05rem !important;
        transition: all .28s ease !important;
    }
    button:hover {
        transform: translateY(-5px);
        border-color:var(--accent) !important;
        color:var(--accent) !important;
        box-shadow:0 18px 45px rgba(124,124,255,.22);
    }
    button:active {
        transform: translateY(-2px) scale(.97);
    }

    .divider {
        display:flex;
        align-items:center;
        margin:3.5rem 0;
        color:var(--muted);
        font-size:.75rem;
        letter-spacing:.18em;
        animation: fadeIn .6s ease-out;
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
        animation: fadeUp 0.8s ease-out both;
    }

    .info {
        background:var(--soft);
        border-radius:18px;
        padding:26px;
        border:1px solid var(--border);
        color:var(--muted);
        animation: fadeIn 1s ease-out;
    }

    @keyframes fadeUp {
        from { opacity:0; transform:translateY(22px); }
        to { opacity:1; transform:translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity:0; }
        to { opacity:1; }
    }
    @keyframes slideIn {
        from { opacity:0; transform:translateX(-28px); }
        to { opacity:1; transform:translateX(0); }
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
    st.markdown(
        "<div class='tagline'>The AI School Assistant<br>From notes to understanding.</div>",
        unsafe_allow_html=True
    )

    if uploaded:
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
        notes = " ".join(page.extract_text() or "" for page in reader.pages)

        if not notes.strip():
            st.error("No readable text found.")
            st.stop()

        st.markdown("### Choose how you want to study")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🧠 Understand", use_container_width=True):
                st.session_state.mode = "summary"
                st.session_state.output = None
                st.session_state.ppt = None

        with c2:
            if st.button("📄 Revise", use_container_width=True):
                st.session_state.mode = "cheat"
                st.session_state.output = None
                st.session_state.ppt = None

        with c3:
            if st.button("📊 Present", use_container_width=True):
                st.session_state.mode = "ppt"
                st.session_state.output = None
                st.session_state.ppt = None

        # ---------- WORKING (UNCHANGED) ----------
        if st.session_state.mode == "summary" and st.session_state.output is None:
            with st.spinner("Reviso is explaining your notes..."):
                st.session_state.output = model.generate_content(
                    f"Create a deep, exam-oriented explanation.\n\nNotes:\n{notes[:15000]}"
                ).text

        if st.session_state.mode == "cheat" and st.session_state.output is None:
            with st.spinner("Reviso is preparing a revision sheet..."):
                st.session_state.output = model.generate_content(
                    f"Create a ONE-PAGE exam cheat sheet.\n\nNotes:\n{notes[:15000]}"
                ).text

        if st.session_state.mode == "ppt" and st.session_state.ppt is None:
            with st.spinner("Reviso is preparing slides..."):
                outline = model.generate_content(
                    f"Create a professional PPT outline.\n\nNotes:\n{notes[:12000]}"
                ).text

                prs = Presentation()
                t = prs.slides.add_slide(prs.slide_layouts[0])
                t.shapes.title.text = "Study Notes"
                t.placeholders[1].text = "Prepared using Reviso"

                for block in outline.split("\n\n"):
                    lines = block.split("\n")
                    if len(lines) < 2:
                        continue
                    s = prs.slides.add_slide(prs.slide_layouts[1])
                    s.shapes.title.text = lines[0][:60]
                    s.placeholders[1].text = "\n".join(lines[1:])

                buf = io.BytesIO()
                prs.save(buf)
                buf.seek(0)
                st.session_state.ppt = buf

        # ---------- OUTPUT ----------
        if st.session_state.output:
            st.markdown("<div class='divider'><span>OUTPUT</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content'>{st.session_state.output}</div>", unsafe_allow_html=True)

        if st.session_state.ppt:
            st.download_button(
                "⬇️ Download Presentation",
                st.session_state.ppt,
                file_name="reviso_presentation.pptx"
            )

    else:
        st.info("Upload your notes to begin.")

with right:
    st.markdown(
        """
        <div class="info">
        <b>Reviso</b><br><br>
        A calm academic assistant designed for
        deep understanding — not shortcuts.
        <br><br>
        • Explain<br>
        • Revise<br>
        • Present
        </div>
        """,
        unsafe_allow_html=True
    )
