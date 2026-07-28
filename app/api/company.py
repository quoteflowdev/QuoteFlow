from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.company import CompanyCreate
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService
from app.core.auth import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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
    company_service = CompanyService()
    saved_company = company_service.create_company(db, db_company)

    return {"message": "Company created successfully",
            "data": saved_company
    }

@router.get("/companies/")
async def get_all_companies(
    db: Session = Depends(get_db)
):
    company_service = CompanyService()
    companies = company_service.get_all_companies(db)

    return {"message": "Companies retrieved successfully",
            "data": companies
    }

@router.get("/companies/{company_id}")
async def get_company_by_id(
    company_id: int,
    db: Session = Depends(get_db)
):
    company_service = CompanyService()
    company = company_service.get_company_by_id(db, company_id)

    if not company:
        return {"message": "Company not found"}

    return {"message": "Company retrieved successfully",
            "data": company
    }


@router.get("/me")
async def get_current_company(
    token: str = Depends(oauth2_scheme)
):
    print("Received Token: ", repr(token))
    payload = verify_access_token(token)

    if not payload:
        return {
            "message": "Invalid or expired token"
        }

    return {
        "message": "Company retrieved successfully",
        "data": {
            "company_id": payload.get("company_id"),
            "email": payload.get("email")
        }
    }

@router.post("/token")
async def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    company_service = CompanyService()

    company = company_service.login_company(
        db,
        form_data.username,
        form_data.password
    )

    if not company:
        return {"message": "Invalid credentials"}

    token = create_access_token({
        "company_id": company.id,
        "email": company.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }