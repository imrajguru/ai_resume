import whisper

model = whisper.load_model("tiny")  # You can also try 'tiny', 'small', etc.

def transcribe_audio(audio_path):
    print("🛠️ Transcribing:", audio_path)  # Add this line
    result = model.transcribe(audio_path)
    return {
        "text": result["text"],
        "segments": result.get("segments", []),
        "language": result.get("language")
    }
