import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_resume_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        return ""

import re 


def guess_candidate_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # First, look for an explicit "Name:" field
    for line in lines[:15]:
        match = re.match(r"^(?:name|candidate name)\s*[:\-]\s*(.+)$",
                         line, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    # Otherwise, look for a likely name near the beginning
    for line in lines[:10]:
        clean_line = line.strip()

        # Ignore common resume information
        if (
            "@" in clean_line
            or clean_line.lower().startswith(("phone", "email", "contact"))
            or any(char.isdigit() for char in clean_line)
            or len(clean_line) > 40
        ):
            continue

        words = clean_line.split()

        if 2 <= len(words) <= 4 and all(
            word.replace(".", "").isalpha() for word in words
        ):
            return clean_line

    return "Unknown Candidate"


