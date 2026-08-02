from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String, nullable=False, index=True)
    owner_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, unique=True, nullable=False, index=True)

    business_type = Column(String, nullable=False)
    company_address = Column(String, nullable=False)

    gst_number = Column(String, unique=True, nullable=True, index=True)

    password = Column(String, nullable=False)

    status = Column(
        String,
        nullable=False,
        default="ACTIVE",
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    customers = relationship(
        "Customer",
        back_populates="company"
    )

    products = relationship(
        "Product",
        foreign_keys="Product.company_id",
        primaryjoin="Company.id == Product.company_id",
        back_populates="company",
        cascade="all, delete-orphan"
    )