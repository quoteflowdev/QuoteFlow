from sqlalchemy import Column, Integer, String
from app.database.connection import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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

Base.metadata.create_all(bind=engine)