from flask import Blueprint, request, jsonify, send_file
from services.report_generator import generate_pdf
import os

report_bp = Blueprint("report", __name__)

@report_bp.route("/score", methods=["POST"])
def generate_score():
    data = request.get_json()
    skills = data.get("skills", [])
    summary = data.get("summary", "")
    from services.ranker import calculate_final_score
    return jsonify(calculate_final_score(skills, summary))

@report_bp.route("/report", methods=["POST"])
def download_pdf():
    data = request.get_json()
    candidate_name = data.get("name", "Candidate")
    skills = data.get("skills", [])
    summary = data.get("summary", "")
    scores = data.get("scores", {})

    strengths = data.get("strengths", [])
    weaknesses = data.get("weaknesses", [])
    suggested_role = data.get("suggested_role", "")

    filename = f"{candidate_name.replace(' ', '_')}_report.pdf"
    save_path = os.path.join("static", filename)

    try:
        generate_pdf(candidate_name, skills, summary, scores, save_path, strengths, weaknesses, suggested_role)
        return send_file(save_path, as_attachment=True)
    except Exception as e:
        print("🔥 PDF Error:", repr(e))
        return jsonify({"error": str(e)}), 500
