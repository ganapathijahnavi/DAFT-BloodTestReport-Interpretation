import os
import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from docx import Document
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    # IMAGE FILES
    if ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file_path).convert("L")
        return pytesseract.image_to_string(image)

    # PDF FILES
    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        # If text-based PDF worked
        if text.strip():
            return text

        # Fallback → scanned PDF
        images = convert_from_path(file_path)
        return "\n".join(
            pytesseract.image_to_string(img.convert("L"))
            for img in images
        )

    # DOCX FILES
    if ext == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    # TXT FILES
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError("Unsupported file format")

