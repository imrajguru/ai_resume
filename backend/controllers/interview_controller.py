from flask import Blueprint, request, jsonify
import os
from services.whisper_transcriber import transcribe_audio
from services.summarizer import generate_summary

interview_bp = Blueprint("interview", __name__)

@interview_bp.route("/upload", methods=["POST"])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename.replace(" ", "_")
    save_path = os.path.abspath(os.path.join("static", filename))

    file.save(save_path)

    # 🔍 Check if the file was actually saved
    if not os.path.isfile(save_path):
        print("🚫 File not saved or cannot be accessed:", save_path)
        return jsonify({"error": "File save failed!"}), 500

    print("📁 Saved file at:", save_path)

    try:
        result = transcribe_audio(save_path)
        return jsonify(result)
    except Exception as e:
        print("🔥 ERROR OCCURRED:", repr(e))
        return jsonify({"error": str(e)}), 500


@interview_bp.route("/summarize", methods=["POST"])
def summarize_transcript():
    data = request.get_json()
    transcript = data.get("transcript", "")

    if not transcript.strip():
        return jsonify({"error": "Transcript is empty"}), 400

    try:
        summary = generate_summary(transcript)
        return jsonify({"summary": summary})
    except Exception as e:
        print("🔥 Summarization ERROR:", repr(e))
        return jsonify({"error": str(e)}), 500

