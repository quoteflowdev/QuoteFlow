from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Enum as SqlEnum,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import Status
from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "phone",
            name="uq_company_phone",
        ),
    )

    __mapper_args__ = {
        "eager_defaults": True
    }

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

    customer_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_name = Column(
        String(100),
        nullable=False,
    )

    phone = Column(
        String(10),
        nullable=False,
        index=True,
    )

    email = Column(
        String(255),
        nullable=True,
        index=True,
    )

    address_line_1 = Column(
        String(255),
        nullable=True,
    )

    address_line_2 = Column(
        String(255),
        nullable=True,
    )

    city = Column(
        String(100),
        nullable=True,
    )

    state = Column(
        String(100),
        nullable=True,
    )

    postal_code = Column(
        String(10),
        nullable=True,
    )

    country = Column(
        String(100),
        nullable=False,
        default="India",
    )

    gst_number = Column(
        String(15),
        nullable=True,
    )

    notes = Column(
        String(500),
        nullable=True,
    )

    status = Column(
        SqlEnum(Status),
        nullable=False,
        default="ACTIVE",
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
        foreign_keys=[company_id],
        back_populates="customers",
    )

    projects = relationship(
        "Project",
        back_populates="customer",
    )