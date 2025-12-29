 📘 Reviso – The AI School Assistant

Reviso is a Streamlit-based AI application that helps students **understand, revise, present, and question their own study notes**.  
By uploading a PDF, students can generate **deep explanations**, **exam-ready cheat sheets**, **presentation slides**, and **context-aware answers**, all powered by Google Gemini.

---

## ✨ Features

- 🧠 **Understand**  
  Generates deep, structured, exam-oriented explanations from notes.

- 📄 **Revise**  
  Creates a concise one-page cheat sheet for quick revision.

- 📊 **Present**  
  Automatically generates a professional PowerPoint presentation from notes.

- ❓ **Ask Questions**  
  Ask natural-language questions and get answers strictly based on the uploaded notes.

- 🔒 **Secure API Handling**  
  Uses environment variables / Streamlit Secrets — no API keys in GitHub.

- ☁️ **Cloud Ready**  
  Deployed on Streamlit Cloud with quota-safe and permission-safe handling.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: Streamlit  
- **AI Model**: Google Gemini (`gemini-1.5-flash`)  
- **PDF Processing**: PyPDF2  
- **Presentation Generation**: python-pptx  
- **Environment Management**: python-dotenv  

---

## 📁 Project Structure

REVISO-AI-SCHOOL-ASSISTANT/
│── intern.py # Main Streamlit app
│── requirements.txt # Dependencies
│── .gitignore # Git ignore rules
│── .env # API key (local only, not committed)

yaml
Copy code

---

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Mohamedzuhair17/REVISO-AI-SCHOOL-ASSISTANT.git
cd REVISO-AI-SCHOOL-ASSISTANT
2️⃣ Create virtual environment (recommended)
bash
Copy code
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Create .env file
env
Copy code
GEMINI_API_KEY=YOUR_API_KEY_HERE
5️⃣ Run the app
bash
Copy code
streamlit run intern.py
☁️ Deployment (Streamlit Cloud)
Push the repository to GitHub

Go to 👉 https://share.streamlit.io

Deploy the repo

Add Secrets:

toml
Copy code
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
Reboot the app

⚠️ Notes on API Usage
The app uses gemini-1.5-flash, the latest publicly available and stable Gemini model.

Input size and request frequency are limited to avoid quota exhaustion.

Graceful error handling is implemented for:

Quota limits

Permission errors

Temporary API unavailability

🎓 Academic Use Case
Reviso is designed for:

Exam preparation

Concept clarification

Quick revision

Presentation preparation

Interactive learning from notes

It is suitable for college projects, demos, and academic submissions.

👨‍💻 Author
Mohamed Zuhair
GitHub: @Mohamedzuhair17

📜 License
This project is for educational purposes.
Feel free to fork and modify for learning and academic use.

markdown
Copy code

---

### ✅ What this README gives you
- Faculty-friendly explanation  
- Clear feature listing  
- Proper deployment instructions  
- Professional GitHub appearance  
- No overclaiming, no fluff  

If you want next:
- Add **screenshots section**
- Add **architecture diagram**
- Add **future scope**
- Make it **IEEE / report-ready**

Just tell me 👍






