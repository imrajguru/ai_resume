import os
import fitz
import docx
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"  # or zephyr / llama3 / your choice

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(filepath)
    elif ext == ".docx":
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file format")

    prompt = f"""
You are an expert recruiter. Analyze the following resume and return the output in JSON format:
- strengths: list of strengths
- weaknesses: list of weaknesses
- skills: list of skills with confidence scores
- suggested_role: most suitable role

Resume:
\"\"\"
{text}
\"\"\"

Respond ONLY in JSON like:
{{
  "strengths": [...],
  "weaknesses": [...],
  "skills": [{{"name": "...", "confidence": 0.85}}],
  "suggested_role": "..."
}}
"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })

        result = response.json()["response"]
        return json.loads(result)
    except Exception as e:
        print("🔥 Local LLM Resume Parsing Error:", e)
        return {
            "strengths": [],
            "weaknesses": [],
            "skills": [],
            "suggested_role": "Unknown"
        }
