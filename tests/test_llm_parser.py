from src.parser import extract_text_from_pdf
from src.llm_parser import structure_shipment_data

text = extract_text_from_pdf(
    "data/sample_invoice.pdf"
)

result = structure_shipment_data(text)

print(result)