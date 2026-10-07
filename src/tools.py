"""
Agent Tools.

This module contains all external tools that can be called
by the AI agent through OpenAI Function Calling.

Available tools:
- parse_document_tool
- db_transport_tool
- calculate_duty_and_currency_tool
"""

from sqlalchemy import func
from src.parser import extract_text_from_pdf
from src.llm_parser import structure_shipment_data
from src.database import (
    Shipment,
    SessionLocal
)


# ==========================================================
# MOCK EXCHANGE RATES
# ==========================================================
#
# For portfolio purposes we use static exchange rates.
# In a production environment these rates should come
# from a real Forex API.
#
# ==========================================================

EXCHANGE_RATES = {
    "USD": 1.00,
    "AUD": 1.52,
    "EUR": 0.91,
    "GBP": 0.78
}


# ==========================================================
# DOCUMENT PARSING TOOL
# ==========================================================

def parse_document_tool(file_path: str) -> dict:
    """
    Parses a logistics PDF document and extracts
    structured shipment data.

    Workflow:
        PDF
          ↓
        Raw Text
          ↓
        LLM Extraction
          ↓
        Structured JSON

    Args:
        file_path (str):
            Path to the PDF document.

    Returns:
        dict:
            Structured shipment information.
    """

    raw_text = extract_text_from_pdf(file_path)

    structured_data = structure_shipment_data(raw_text)

    return structured_data


# ==========================================================
# DUTY & CURRENCY TOOL
# ==========================================================

def calculate_duty_and_currency_tool(
    amount_usd: float,
    target_currency: str
) -> dict:
    """
    Converts a USD amount into another currency
    and adds a flat customs duty of 10%.

    Args:
        amount_usd (float):
            Original amount in USD.

        target_currency (str):
            Target currency code.
            Example:
                AUD
                EUR
                GBP

    Returns:
        dict:
            Calculation results.
    """

    currency = target_currency.upper()

    exchange_rate = EXCHANGE_RATES.get(currency)

    if exchange_rate is None:
        raise ValueError(
            f"Unsupported currency: {currency}"
        )

    converted_amount = amount_usd * exchange_rate

    customs_duty = converted_amount * 0.10

    total_amount = converted_amount + customs_duty

    return {
        "original_usd": amount_usd,
        "currency": currency,
        "exchange_rate": exchange_rate,
        "converted_amount": round(
            converted_amount,
            2
        ),
        "customs_duty": round(
            customs_duty,
            2
        ),
        "total_amount": round(
            total_amount,
            2
        )
    }


# ==========================================================
# DATABASE TOOL
# ==========================================================

def db_transport_tool(
    action: str,
    payload: dict
):
    """
    Executes database operations.

    Supported actions:

    - create
    - list
    - filter_destination

    Args:
        action (str):
            Database action.

        payload (dict):
            Data required by the action.

    Returns:
        dict or list
    """

    db = SessionLocal()

    try:

        # ==================================================
        # CREATE SHIPMENT
        # ==================================================

        if action == "create":
            
            existing_shipment = (
                db.query(Shipment)
                .filter(
                    Shipment.tracking_number ==
                    payload["tracking_number"]
                )
                .first()
            )

            if existing_shipment:

                return {
                    "status": "already_exists",
                    "message": (
                        f"Shipment "
                        f"{payload['tracking_number']} "
                        f"already exists."
                    ),
                    "shipment_id": existing_shipment.id
                }

            shipment = Shipment(**payload)

            db.add(shipment)

            db.commit()

            db.refresh(shipment)

            return {
                "status": "success",
                "shipment_id": shipment.id,
                "tracking_number": shipment.tracking_number
            }

        # ==================================================
        # COUNT SHIPMENTS
        # ==================================================

        if action == "count":

            total_shipments = (
                db.query(Shipment)
                .count()
            )

            return {
                "total_shipments": total_shipments
            }

        # ==================================================
        # AVERAGE SHIPPING COST
        # ==================================================

        if action == "average_cost":

            average_cost = (
                db.query(
                    func.avg(
                        Shipment.shipping_cost
                    )
                )
                .scalar()
            )

            return {
                "average_shipping_cost": round(
                    float(average_cost),
                    2
                )
            }
    
        # ==================================================
        # LIST ALL SHIPMENTS
        # ==================================================

        if action == "list":

            shipments = db.query(
                Shipment
            ).all()

            return [
                shipment.to_dict()
                for shipment in shipments
            ]

        # ==================================================
        # LIST COUNTRIES
        # ==================================================

        if action == "list_countries":

            countries = (
                db.query(
                    Shipment.destination_country
                )
                .distinct()
                .all()
            )

            return {
                "countries": [
                    country[0]
                    for country in countries
                ]
            }
    
        # ==================================================
        # LIST TRANSPORT MODES
        # ==================================================

        if action == "list_transport_modes":

            transport_modes = (
                db.query(
                    Shipment.transport_mode
                )
                .distinct()
                .all()
            )

            return {
                "transport_modes": [
                    mode[0]
                    for mode in transport_modes
                ]
            }
    
        # ==================================================
        # FILTER BY DESTINATION COUNTRY
        # ==================================================

        if action == "filter_destination":

            country = payload.get("country")

            shipments = (
                db.query(Shipment)
                .filter(
                    Shipment.destination_country == country
                )
                .all()
            )

            return [
                shipment.to_dict()
                for shipment in shipments
            ]

        # ==================================================
        # UNSUPPORTED ACTION
        # ==================================================

        raise ValueError(
            f"Unsupported action: {action}"
        )

    finally:

        db.close()


# ==========================================================
# OPENAI FUNCTION DEFINITIONS
# ==========================================================
#
# These schemas will be sent to OpenAI.
# GPT will decide automatically which tool
# should be executed.
#
# ==========================================================

OPENAI_TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "parse_document_tool",
            "description": (
                "Extract shipment information from "
                "a logistics PDF document."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "Path to the PDF file."
                        )
                    }
                },
                "required": [
                    "file_path"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "db_transport_tool",
            "description": (
                "Perform operations on the "
                "shipment database."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "action": {
                        "type": "string",
                        "enum": [
                            "create",
                            "list",
                            "filter_destination",
                            "count",
                            "average_cost",
                            "list_countries",
                            "list_transport_modes"
                        ]
                    },

                    "payload": {
                        "type": "object"
                    }

                },
                "required": [
                    "action",
                    "payload"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": (
                "calculate_duty_and_currency_tool"
            ),
            "description": (
                "Convert USD amount into another "
                "currency and apply customs duty."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "amount_usd": {
                        "type": "number"
                    },

                    "target_currency": {
                        "type": "string"
                    }

                },
                "required": [
                    "amount_usd",
                    "target_currency"
                ]
            }
        }
    }

]