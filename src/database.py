"""
Database layer.

This module contains:
- SQLAlchemy configuration
- Session management
- Shipment ORM model
- Database initialization helpers
"""

from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

from src.config import settings


# ------------------------------------------------------------------
# Database Engine
# ------------------------------------------------------------------
# Creates the connection to SQLite.
#
# check_same_thread=False is required because FastAPI
# may handle requests across multiple threads.
# ------------------------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ------------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------------
# Every database interaction will use one session.
# FastAPI will later inject these sessions automatically.
# ------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# ------------------------------------------------------------------
# Base ORM Class
# ------------------------------------------------------------------
# Every ORM model inherits from Base.
# ------------------------------------------------------------------

Base = declarative_base()


# ------------------------------------------------------------------
# Shipment Model
# ------------------------------------------------------------------

class Shipment(Base):
    """
    Represents a freight shipment stored in the database.
    """

    __tablename__ = "shipments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tracking_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    sender = Column(
        String(255),
        nullable=False
    )

    recipient = Column(
        String(255),
        nullable=False
    )

    destination_country = Column(
        String(100),
        nullable=False,
        index=True
    )

    transport_mode = Column(
        String(50),
        nullable=True
    )

    incoterm = Column(
        String(20),
        nullable=True
    )

    weight_kg = Column(
        Float,
        nullable=False
    )

    shipping_cost = Column(
        Float,
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False,
        default="USD"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    def to_dict(self) -> dict:
        """
        Converts the ORM object to a serializable dictionary.
        """

        return {
            "id": self.id,
            "tracking_number": self.tracking_number,
            "sender": self.sender,
            "recipient": self.recipient,
            "destination_country": self.destination_country,
            "transport_mode": self.transport_mode,
            "incoterm": self.incoterm,
            "weight_kg": self.weight_kg,
            "shipping_cost": self.shipping_cost,
            "currency": self.currency,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


# ------------------------------------------------------------------
# Database Initialization
# ------------------------------------------------------------------

def init_db() -> None:
    """
    Creates all missing database tables.
    """

    Base.metadata.create_all(bind=engine)


# ------------------------------------------------------------------
# FastAPI Dependency
# ------------------------------------------------------------------

def get_db():
    """
    Provides a database session.

    Later, FastAPI endpoints will use:

        Depends(get_db)
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()