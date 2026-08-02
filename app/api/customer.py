from fastapi import (APIRouter, Depends, HTTPException, Query, status)
from sqlalchemy.orm import Session

from app.core.auth import get_current_company
from app.database.connection import get_db
from app.models.company import Company
from app.schemas.customer import (CustomerCreate, CustomerResponse, CustomerUpdate)
from app.services.customer_service import CustomerService


router = APIRouter()

customer_service = CustomerService()


@router.post("/customers/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED,)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    saved_customer = customer_service.create_customer(
        db=db,
        company_id=current_company.id,
        customer_data=customer,
    )

    if saved_customer is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with this phone number or email already exists.",
        )

    return saved_customer


@router.get("/customers/", response_model=list[CustomerResponse],)
async def get_all_customers(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return customer_service.get_all_customers(
        db=db,
        company_id=current_company.id,
    )


@router.get("/customers/search/", response_model=list[CustomerResponse],)
async def search_customers(
    search: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return customer_service.search_customers(
        db=db,
        company_id=current_company.id,
        search=search,
        page=page,
        limit=limit,
    )


@router.get("/customers/{customer_id}", response_model=CustomerResponse,)
async def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    customer = customer_service.get_customer_by_id(
        db=db,
        company_id=current_company.id,
        customer_id=customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer


@router.put("/customers/{customer_id}", response_model=CustomerResponse,)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    customer = customer_service.update_customer(
        db=db,
        company_id=current_company.id,
        customer_id=customer_id,
        customer_update=customer_update,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or phone/email already exists.",
        )

    return customer


@router.patch("/customers/{customer_id}/deactivate", response_model=CustomerResponse,)
async def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    customer = customer_service.deactivate_customer(
        db=db,
        company_id=current_company.id,
        customer_id=customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer


@router.patch("/customers/{customer_id}/restore", response_model=CustomerResponse,)
async def restore_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    customer = customer_service.restore_customer(
        db=db,
        company_id=current_company.id,
        customer_id=customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer