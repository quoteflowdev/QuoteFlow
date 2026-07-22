from pydantic import BaseModel, EmailStr

class CompanyCreate(BaseModel):
    company_name: str
    owner_name: str
    email: EmailStr
    phone_number: str
    business_type: str
    company_address: str
    gst_number: str
    password: str