# model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# -------------------------------
# MODEL CONFIG
# -------------------------------
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_MODEL = "ganapati-jahnavi/tinylamma-medical-bloodtest"

DEVICE = "cpu"  # HF Spaces CPU safe
DTYPE = torch.float32


# -------------------------------
# LOAD TOKENIZER
# -------------------------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# -------------------------------
# LOAD BASE MODEL
# -------------------------------
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=DTYPE,
    device_map=None
)

# -------------------------------
# LOAD YOUR FINE-TUNED LoRA ADAPTER
# -------------------------------
model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_MODEL
)

model.to(DEVICE)
model.eval()


# ======================================================
# MAIN MEDICAL INTERPRETATION FUNCTION
# ======================================================
def run_medical_model(context_text: str) -> str:
    prompt = f"""
You are a medical AI assistant.

Based on the abnormal laboratory findings listed below, provide a clear and concise medical interpretation.

Guidelines:
- Use bullet points
- Explain possible clinical significance
- Mention common conditions (not a diagnosis)
- Provide general lifestyle guidance
- Suggest follow-up tests if relevant
- Do NOT repeat instructions
- Do NOT repeat the lab report

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
            max_new_tokens=350,
            min_new_tokens=120,
            temperature=0.4,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove prompt safely
    if "Medical Interpretation:" in decoded:
        decoded = decoded.split("Medical Interpretation:")[-1].strip()

    # Guard against empty / echoed output
    if len(decoded.strip()) < 30:
        decoded = (
            "- The reported abnormalities suggest physiological imbalance.\n"
            "- These findings commonly require clinical correlation.\n"
            "- Follow-up testing and physician consultation are advised."
        )

    # Append disclaimer once
    decoded += (
        "\n\n⚠️ Disclaimer: This is an AI-generated educational summary. "
        "It is not a medical diagnosis. Please consult a qualified physician."
    )

    return decoded


# ======================================================
# CHAT ABOUT REPORT FUNCTION
# ======================================================
def chat_about_report(report_context: str, user_question: str) -> str:
    prompt = f"""
You are a medical AI assistant helping a patient understand their blood test report.

Medical Report Data:
{report_context}

Patient Question: {user_question}

Provide a clear, helpful answer based on the report data above. Keep your response:
- Focused on the patient's specific question
- Clear and easy to understand
- Based only on the information in the report
- Include relevant medical context

Answer:
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
            max_new_tokens=250,
            min_new_tokens=50,
            temperature=0.5,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.3,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Answer:" in decoded:
        decoded = decoded.split("Answer:")[-1].strip()

    if len(decoded.strip()) < 20:
        decoded = (
            "I'm unable to provide a specific answer based on the report data. "
            "Please consult with your healthcare provider for detailed medical advice."
        )

    return decoded
