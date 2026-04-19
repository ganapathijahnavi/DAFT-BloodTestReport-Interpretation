# model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# -------------------------------
# MODEL CONFIG
# -------------------------------
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_MODEL = "ganapati-jahnavi/tinylamma-medical-bloodtest"

DEVICE = "cpu"
DTYPE = torch.float32

print("🔥 MODEL LOADING...")

# -------------------------------
# TOKENIZER
# -------------------------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# -------------------------------
# MODEL
# -------------------------------
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=DTYPE
)

model = PeftModel.from_pretrained(base_model, ADAPTER_MODEL)
model.to(DEVICE)
model.eval()

print("✅ MODEL READY")


# ======================================================
# MAIN FUNCTION (MINIMAL CONTROL, MODEL DRIVEN)
# ======================================================
def run_medical_model(context_text: str) -> str:
    prompt = f"""
You are a medical AI assistant.
Write a structured medical interpretation in a professional report style.
Format:
1. Start with a short paragraph summary (no bullets)
2. Then include these sections (if relevant):
   Clinical Significance:
   Suggested Follow Up:
   Recommendations:
Rules:
- Use bullet points under sections
- Do NOT ask questions
- Do NOT write "Answer:" or "Question:"
- Do NOT repeat content
- Keep it concise and clear
Abnormal Findings:
{context_text}
Medical Interpretation:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.3,      # 🔥 more stable
            do_sample=True,
            top_p=0.8,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # -------------------------------
    # REMOVE PROMPT
    # -------------------------------
    if "Medical Interpretation:" in decoded:
        cleaned = decoded.split("Medical Interpretation:", 1)[-1].strip()
    else:
        cleaned = decoded.replace(prompt, "").strip()

    # -------------------------------
    # REMOVE BAD PATTERNS (LIGHT CLEAN)
    # -------------------------------
    garbage = ["Answer:", "Question:", "Explanation:", "Based on the passage"]

    for g in garbage:
        cleaned = cleaned.replace(g, "")

    # -------------------------------
    # REMOVE DUPLICATE LINES
    # -------------------------------
    lines = []
    seen = set()

    for line in cleaned.split("\n"):
        line = line.strip()
        if line and line not in seen:
            lines.append(line)
            seen.add(line)

    final_output = "\n".join(lines)

    # -------------------------------
    # APPEND DISCLAIMER
    # -------------------------------
    final_output += "\n\nDisclaimer: This is an AI-generated summary. It is not a medical diagnosis."

    return final_output


# ======================================================
# CHAT FUNCTION (UNCHANGED LOGIC)
# ======================================================
def chat_about_report(report_context: str, user_question: str) -> str:
    prompt = f"""
You are a medical AI assistant.
Answer clearly in simple terms.
Report:
{report_context}
Question:
{user_question}
Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            temperature=0.4,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Answer:" in decoded:
        decoded = decoded.split("Answer:", 1)[-1].strip()

    return decoded
