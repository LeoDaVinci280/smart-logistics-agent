"""
Populate the database with sample logistics data.

Run once to generate a realistic dataset
for AI agent demonstrations.
"""

from src.database import (
    SessionLocal,
    Shipment
)

db = SessionLocal()

sample_shipments = [

    {
        "tracking_number": "TRK1001",
        "sender": "Amazon USA",
        "recipient": "Sydney Warehouse",
        "destination_country": "Australia",
        "transport_mode": "Sea",
        "incoterm": "CIF",
        "weight_kg": 500,
        "shipping_cost": 1200,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1002",
        "sender": "Dell USA",
        "recipient": "Melbourne DC",
        "destination_country": "Australia",
        "transport_mode": "Air",
        "incoterm": "DAP",
        "weight_kg": 85,
        "shipping_cost": 950,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1003",
        "sender": "Bosch Germany",
        "recipient": "Paris Hub",
        "destination_country": "France",
        "transport_mode": "Road",
        "incoterm": "DDP",
        "weight_kg": 200,
        "shipping_cost": 350,
        "currency": "EUR"
    },

    {
        "tracking_number": "TRK1004",
        "sender": "Samsung Korea",
        "recipient": "Berlin Warehouse",
        "destination_country": "Germany",
        "transport_mode": "Sea",
        "incoterm": "FOB",
        "weight_kg": 1200,
        "shipping_cost": 2800,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1005",
        "sender": "Foxconn China",
        "recipient": "London DC",
        "destination_country": "United Kingdom",
        "transport_mode": "Air",
        "incoterm": "CIP",
        "weight_kg": 150,
        "shipping_cost": 1800,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1006",
        "sender": "Tesla USA",
        "recipient": "Toronto Facility",
        "destination_country": "Canada",
        "transport_mode": "Road",
        "incoterm": "DAP",
        "weight_kg": 750,
        "shipping_cost": 900,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1007",
        "sender": "Alibaba China",
        "recipient": "Singapore Hub",
        "destination_country": "Singapore",
        "transport_mode": "Sea",
        "incoterm": "EXW",
        "weight_kg": 1800,
        "shipping_cost": 3400,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1008",
        "sender": "Siemens Germany",
        "recipient": "Dubai Logistics Park",
        "destination_country": "United Arab Emirates",
        "transport_mode": "Air",
        "incoterm": "DDP",
        "weight_kg": 250,
        "shipping_cost": 2100,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1009",
        "sender": "Toyota Japan",
        "recipient": "Auckland DC",
        "destination_country": "New Zealand",
        "transport_mode": "Sea",
        "incoterm": "CIF",
        "weight_kg": 950,
        "shipping_cost": 2600,
        "currency": "USD"
    },

    {
        "tracking_number": "TRK1010",
        "sender": "Apple USA",
        "recipient": "Madrid Warehouse",
        "destination_country": "Spain",
        "transport_mode": "Air",
        "incoterm": "DAP",
        "weight_kg": 120,
        "shipping_cost": 1100,
        "currency": "USD"
    }
]


for shipment_data in sample_shipments:

    exists = (
        db.query(Shipment)
        .filter(
            Shipment.tracking_number ==
            shipment_data["tracking_number"]
        )
        .first()
    )

    if not exists:

        db.add(
            Shipment(**shipment_data)
        )

db.commit()
db.close()

print(
    f"{len(sample_shipments)} sample shipments processed."
)