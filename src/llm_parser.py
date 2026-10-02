"""
LLM-powered document structuring.
"""

import json

from openai import OpenAI

from src.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def structure_shipment_data(document_text: str) -> dict:
    """
    Convert raw logistics text into structured JSON.
    """

    try:

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract shipment information as JSON."
                    )
                },
                {
                    "role": "user",
                    "content": document_text
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        return json.loads(
            response.choices[0].message.content
        )

    except Exception as ex:

        return {
            "error": str(ex),
            "tracking_number": None,
            "sender": None,
            "recipient": None,
            "destination_country": None,
            "weight_kg": None,
            "shipping_cost": None,
            "currency": None
        }