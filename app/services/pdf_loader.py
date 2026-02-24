import os
from PyPDF2 import PdfReader

def load_pdf(file_path: str):
    reader = PdfReader("data/documents")
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text
