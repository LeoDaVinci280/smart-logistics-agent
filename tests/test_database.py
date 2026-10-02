"""
Simple database test.

Purpose:
- Create database
- Insert a shipment
- Verify SQLAlchemy works correctly
"""

from src.database import (
    init_db,
    Shipment,
    SessionLocal
)

# Create tables if they do not exist
init_db()

# Open database session
db = SessionLocal()

shipment = Shipment(
    tracking_number="TRK0001",
    sender="Amazon USA",
    recipient="Sydney Warehouse",
    destination_country="Australia",
    transport_mode="Sea",
    incoterm="CIF",
    weight_kg=500,
    shipping_cost=1200,
    currency="USD"
)

db.add(shipment)
db.commit()

print("Shipment inserted successfully!")

db.close()