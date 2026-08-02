from sqlalchemy import (Boolean, Column, DateTime, Enum as SqlEnum, Integer, String, ForeignKey, UniqueConstraint,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import (CalculationType, Status, Unit,)
from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "product_name",
            name="uq_company_product_name",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
    )

    product_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    product_name = Column(
        String(100),
        nullable=False,
    )

    calculation_type = Column(
        SqlEnum(CalculationType),
        nullable=False,
    )

    default_unit = Column(
        SqlEnum(Unit),
        nullable=False,
    )

    allow_decimal = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    icon = Column(
        String(50),
        nullable=True,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    is_system = Column(
        Boolean,
        nullable=False,
        default=False,
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
        foreign_keys=[company_id],
        back_populates="products",
    )