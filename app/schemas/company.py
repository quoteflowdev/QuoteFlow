from datetime import datetime

from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    company_name: str
    owner_name: str
    email: EmailStr
    phone_number: str
    business_type: str
    company_address: str
    gst_number: str


class CompanyCreate(CompanyBase):
    password: str


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str