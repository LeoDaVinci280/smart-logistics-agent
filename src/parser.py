"""
Document parsing utilities.

This module is responsible for:
- Extracting text from PDF files
- Returning raw text for further AI processing
"""

from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF document.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A string containing all extracted text.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    reader = PdfReader(file_path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)