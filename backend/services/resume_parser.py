import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    doc = nlp(text)
    skills = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE", "LANGUAGE"]:  # Approximate for demo
            skills.append(ent.text)
    return list(set(skills))

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    return {
        "raw_text": text,
        "extracted_skills": skills
    }
