from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.connection import engine
from app.database.base import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, index=True)
    owner_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    business_type = Column(String)
    company_address = Column(String)
    gst_number = Column(String, unique=True, index=True)
    password = Column(String)  # Store hashed password in production

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customers = relationship("Customer", back_populates="company")
Base.metadata.create_all(bind=engine)
