from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyBase(BaseModel):
    company_name: str
    owner_name: str
    email: EmailStr
    phone_number: str
    business_type: str
    company_address: str
    gst_number: Optional[str] = None


class CompanyCreate(CompanyBase):
    password: str


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    owner_name: Optional[str] = None
    business_type: Optional[str] = None
    company_address: Optional[str] = None
    gst_number: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
