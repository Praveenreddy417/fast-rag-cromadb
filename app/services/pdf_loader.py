import os
from PyPDF2 import PdfReader


def load_pdfs_from_directory(directory_path: str) -> str:
    """
    Load and extract text from all PDF files inside a directory.
    """

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    all_text = ""

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)

            print(f"Reading: {file_path}")

            reader = PdfReader(file_path)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"

    return all_text
