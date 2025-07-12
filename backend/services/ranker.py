from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Keywords your job requires (for now hardcoded)
job_keywords = [
    "python", "machine learning", "flask", "react", "apis", "database", "node.js"
]

def calculate_resume_score(skills: list) -> float:
    matched = [s for s in skills if s.lower() in job_keywords]
    return round((len(matched) / len(job_keywords)) * 100, 2)

def calculate_summary_score(summary: str) -> float:
    reference = " ".join(job_keywords)
    vectorizer = TfidfVectorizer().fit_transform([summary, reference])
    score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    return round(score * 100, 2)

def calculate_final_score(resume_skills: list, summary_text: str) -> dict:
    resume_score = calculate_resume_score(resume_skills)
    summary_score = calculate_summary_score(summary_text)
    final_score = round((resume_score * 0.5) + (summary_score * 0.5), 2)

    return {
        "resume_score": resume_score,
        "summary_score": summary_score,
        "final_score": final_score
    }
