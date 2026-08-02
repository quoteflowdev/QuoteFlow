from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import (create_access_token, get_current_company)
from app.database.connection import get_db
from app.models.company import Company
from app.schemas.company import (CompanyCreate, CompanyResponse, CompanyUpdate)
from app.services.auth_services import AuthService
from app.services.company_service import CompanyService


router = APIRouter()

company_service = CompanyService()
auth_service = AuthService()


@router.post("/companies/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):

    try:

        saved_company = company_service.create_company(
            db,
            company
        )

        return saved_company
        

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/companies/", response_model=list[CompanyResponse])
async def get_all_companies(
    db: Session = Depends(get_db)
):

    companies = company_service.get_all_companies(
        db
    )

    return companies
    


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company_by_id(
    company_id: int,
    db: Session = Depends(get_db)
):

    company = company_service.get_company_by_id(
        db,
        company_id
    )

    if company is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found."
        )

    return company
    


@router.get("/me", response_model=CompanyResponse)
async def me(
    current_company: Company = Depends(get_current_company)
):

    return current_company
    


@router.post("/token")
async def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    company = auth_service.authenticate_company(
        db,
        form_data.username,   # username = phone number
        form_data.password
    )

    if company is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password."
        )

    token = create_access_token(
        {
            "company_id": company.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.put("/companies/profile", response_model=CompanyResponse)
async def update_company(
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):

    updated_company = company_service.update_company(
        db,
        current_company.id,
        company_update
    )

    if updated_company is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found."
        )

    return updated_company


@router.patch("/deactivate")
async def deactivate_company(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):

    company = company_service.deactivate_company(
        db,
        current_company.id
    )

    if company is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found."
        )

    return {
        "message": "Company account deactivated successfully."
    }