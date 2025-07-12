
# 🧠 AI-Powered Candidate Evaluation System

This project evaluates candidates by parsing their resumes and interview audio using AI. It uses **local LLMs (via Ollama)** to extract skills, strengths, weaknesses, and recommends job roles. The system generates a professional PDF report summarizing the evaluation.

---

## 🔥 Features

✅ Resume parsing using LLaMA/Zephyr via [Ollama](https://ollama.com)  
✅ Interview transcription using [Whisper](https://github.com/openai/whisper)  
✅ Intelligent scoring based on resume and interview summary  
✅ Final PDF report with:
- Scores
- Strengths & weaknesses
- Extracted skills
- Suggested job role
- Summary
- Bar chart visualization

✅ Simple Streamlit-based frontend  
✅ Runs entirely **offline** (no OpenAI API needed)

---

## 🗂️ Project Structure

```
ai-resume-evaluator/
├── backend/
│   ├── app.py
│   ├── controllers/
│   ├── services/
│   ├── utils/
│   ├── config/
│   ├── static/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── app.py
├── DejaVuSans.ttf
├── README.md
└── .gitignore
```

---

## 🛠️ Setup Instructions

### 🔹 Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally (`ollama run llama3`)

### 🔹 1. Backend Setup

```bash
cd backend
python -m venv env
env\Scripts\activate   # On Windows

pip install -r requirements.txt
```

> Make sure `DejaVuSans.ttf` is placed in the root or same folder as `report_generator.py` to support Unicode in PDF.

### 🔹 2. Frontend Setup

```bash
cd ../frontend
streamlit run app.py
```

---

## 🔐 Environment Variables

> No external APIs are used. You can use `.env.example` to document any custom variables (like LLaMA model name), if needed.

---

## 📄 Sample PDF Report Includes:

- ✅ Resume Score
- ✅ Interview Summary Score
- ✅ Final Score
- ✅ Strengths / Weaknesses
- ✅ Suggested Role
- ✅ Skill list
- ✅ Bar chart breakdown

---

## 📦 Key Tech Stack

| Component | Tool |
|----------|------|
| LLM | LLaMA via Ollama |
| Transcription | Whisper |
| PDF Report | fpdf2 + matplotlib |
| Frontend | Streamlit |
| Backend | Flask |
| LLM Reasoning | Local JSON prompt from resume |

---

## 🧪 Example Usage

Upload a `.pdf` or `.docx` resume  
(Optional) Upload a `.wav` interview audio  
Click "🚀 Generate Report"  
Download the generated PDF

---

## 📸 Screenshot

_You can add a UI screenshot or sample PDF output here_

---

## 👨‍💻 Developed By

Made with 💻 + 🧠 by **Rajguru Thevar**  
Feel free to fork, contribute, or reuse for your own project!

---
