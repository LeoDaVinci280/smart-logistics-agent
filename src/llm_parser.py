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
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is not configured."
        )

    try:

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a logistics data extraction assistant. "
                        "Extract shipment data and return valid JSON only. "
                        "Extract transport mode and incoterm whenever available. "
                        "Use EXACTLY the following schema: "
                        "{"
                        "\"tracking_number\": string,"
                        "\"sender\": string,"
                        "\"recipient\": string,"
                        "\"destination_country\": string,"
                        "\"transport_mode\": string,"
                        "\"incoterm\": string,"
                        "\"weight_kg\": number,"
                        "\"shipping_cost\": number,"
                        "\"currency\": string"
                        "} "
                        "Never use alternative field names."
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
            "transport_mode": None,
            "incoterm": None,
            "weight_kg": None,
            "shipping_cost": None,
            "currency": None
        }