from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


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
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)