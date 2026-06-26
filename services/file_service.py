import os
from PyPDF2 import PdfReader

try:
    from docx import Document
    DOCX_AVAILABLE = True
except:
    DOCX_AVAILABLE = False


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        return text

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".docx") and DOCX_AVAILABLE:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


def get_preview(text):
    lines = text.splitlines()
    return "\n".join(lines[:5])