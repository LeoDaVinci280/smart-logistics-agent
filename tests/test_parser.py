from src.parser import extract_text_from_pdf

text = extract_text_from_pdf(
    "data/sample_invoice.pdf"
)

print(text)