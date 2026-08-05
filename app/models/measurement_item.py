from sqlalchemy import (Column, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import Status
from app.database.base import Base


class MeasurementItem(Base):
    __tablename__ = "measurement_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    measurement_id = Column(
        Integer,
        ForeignKey("measurements.id"),
        nullable=False,
        index=True,
    )

    location = Column(
        String(150),
        nullable=False,
    )

    # Height
    height_feet = Column(
        Integer,
        nullable=True,
    )

    height_inch = Column(
        Float,
        nullable=True,
        default=0,
    )

    # Width
    width_feet = Column(
        Integer,
        nullable=True,
    )

    width_inch = Column(
        Float,
        nullable=True,
        default=0,
    )

    # Length
    length_feet = Column(
        Integer,
        nullable=True,
    )

    length_inch = Column(
        Float,
        nullable=True,
        default=0,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
    )

    # Single Piece Result
    unit_value = Column(
        Float,
        nullable=False,
        default=0,
    )

    # Final Result (Unit × Qty)
    calculated_value = Column(
        Float,
        nullable=False,
        default=0,
    )

    remarks = Column(
        String(300),
        nullable=True,
    )

    status = Column(
        SqlEnum(Status),
        nullable=False,
        default=Status.ACTIVE,
        index=True,
    )

    created_by = Column(
        Integer,
        nullable=True,
    )

    updated_by = Column(
        Integer,
        nullable=True,
    )

    version = Column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    measurement = relationship(
        "Measurement",
        back_populates="items",
    )