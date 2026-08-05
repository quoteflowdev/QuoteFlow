from sqlalchemy import (Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import Status
from app.database.base import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    measurement_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    measurement_name = Column(
        String(150),
        nullable=False,
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

    company = relationship(
        "Company",
        back_populates="measurements",
    )

    project = relationship(
        "Project",
        back_populates="measurements",
    )

    product = relationship(
        "Product",
        back_populates="measurements",
    )

    items = relationship(
        "MeasurementItem",
        back_populates="measurement",
        cascade="all, delete-orphan",
    )