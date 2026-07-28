from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(10),
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True
    )

    address_line_1 = Column(
        String(255),
        nullable=True
    )

    address_line_2 = Column(
        String(255),
        nullable=True
    )

    city = Column(
        String(100),
        nullable=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    postal_code = Column(
        String(10),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    gst_number = Column(
        String(15),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    company = relationship(
        "Company",
        back_populates="customers"
    )


