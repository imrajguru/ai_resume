from flask import Blueprint, request, jsonify
import os
from services.resume_parser_llm import parse_resume

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/upload", methods=["POST"])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    save_path = os.path.join("static", file.filename)
    file.save(save_path)

    try:
        result = parse_resume(save_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
