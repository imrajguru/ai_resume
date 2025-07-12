from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load T5 model
model_name = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_summary(transcript: str) -> str:
    # Instruction-style prompt
    prompt = "summarize: " + transcript.strip()

    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs,
        max_length=100,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary
