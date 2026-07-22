from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.company import CompanyCreate
from app.models.company import Company

router = APIRouter()

@router.post("/companies/")
async def create_company(
    company: CompanyCreate, 
    db: Session = Depends(get_db)
):

    db_company = Company(
        company_name=company.company_name,
        owner_name=company.owner_name,
        email=company.email,
        phone_number=company.phone_number,
        business_type=company.business_type,
        company_address=company.company_address,
        gst_number=company.gst_number,
        password=company.password  # In production, hash the password before storing
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return {"message": "Company created successfully",
            "data": company
    }
