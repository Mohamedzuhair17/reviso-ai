<!-- EFFECTS-BLOCK:START -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=F6F1EA&height=180&section=header&text=Reviso%20Ai&fontSize=44&fontColor=111111&desc=LLM-powered%20knowledge%20extraction%20pipeline%20converting%20raw%20academic%20content%20into%20structured%20study%20assets.&descSize=14&descAlignY=68" alt="Reviso Ai" />
</p>

<p align="center">
  <a href="https://github.com/Mohamedzuhair17/reviso-ai"><img src="https://img.shields.io/badge/Repository-111111?style=for-the-badge&logo=github" alt="repo" /></a>
  <img src="https://img.shields.io/github/stars/Mohamedzuhair17/=for-the-badge&color=111111" alt="stars" />
  <img src="https://img.shields.io/github/forks/Mohamedzuhair17/=for-the-badge&color=111111" alt="forks" />
  <img src="https://img.shields.io/github/last-commit/Mohamedzuhair17/=for-the-badge&color=111111" alt="last commit" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Stack-Python-F6F1EA?style=for-the-badge&labelColor=111111&color=F6F1EA" alt="stack" />
  <img src="https://img.shields.io/badge/Engineering-Production%20Grade-111111?style=for-the-badge" alt="engineering" />
</p>
<!-- EFFECTS-BLOCK:END -->

---

📘 Reviso – The AI School Assistant
Learn smarter. Revise faster. Present better.

Reviso is an AI-powered academic assistant built with Streamlit that helps students understand, revise, present, and question their own study notes — all from a single uploaded PDF.
Powered by Google Gemini, Reviso transforms study materials into deep explanations, concise summaries, professional slides, and context-aware Q&A.

✨ Key Features
🧠 Understand: Generate detailed, structured, exam-oriented explanations from your notes.

📄 Revise: Create a clear, one-page cheat sheet for instant review.

📊 Present: Automatically build professional PowerPoint slides from your material.

❓ Ask Questions: Get natural-language answers strictly based on your uploaded notes.

🔒 Secure API Handling: API keys are managed via environment variables / Streamlit Secrets — never exposed in code.

☁️ Cloud Ready: Fully deployable on Streamlit Cloud with safe quota and permission handling.

🛠️ Tech Stack
Frontend & Framework: Streamlit

AI Model: Google Gemini (gemini-1.5-flash)

PDF Parsing: PyPDF2

Presentation Builder: python-pptx

Env Management: python-dotenv

📁 Project Structure
text
REVISO-AI-SCHOOL-ASSISTANT/
│── intern.py              # Main Streamlit app
│── requirements.txt       # Dependencies
│── .gitignore             # Git ignore rules
│── .env                   # Local API key storage (not committed)
🚀 Local Setup
1️⃣ Clone the repository

bash
git clone https://github.com/Mohamedzuhair17/REVISO-AI-SCHOOL-ASSISTANT.git
cd REVISO-AI-SCHOOL-ASSISTANT
2️⃣ Create a virtual environment

bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
3️⃣ Install dependencies

bash
pip install -r requirements.txt
4️⃣ Add your API key to .env

text
GEMINI_API_KEY=YOUR_API_KEY_HERE
5️⃣ Run the app

bash
streamlit run intern.py
☁️ Deploy on Streamlit Cloud
Push your repo to GitHub

Visit Streamlit Cloud

Deploy the repository

Add the following secret:

text
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
Reboot the app and you’re live 🎉

⚠️ Notes on Usage
The app uses gemini-1.5-flash, the latest stable model.
It includes safeguards for:

Quota limits

Permission errors

Temporary unavailability

Error messages are gracefully handled for a smooth learning experience.

🎓 Academic Applications
Ideal for:

Exam preparation & note summarization

Concept clarification for study sessions

Presentation generation for assignments

Interactive Q&A learning from course material

Perfect for college projects, academic demos, and learning showcases.

👨‍💻 Author
Mohamed Zuhair
GitHub: @Mohamedzuhair17

📜 This project is for educational use. Feel free to fork and modify for your academic or learning purposes.

