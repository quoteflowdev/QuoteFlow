from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.services.customer_service import CustomerService
from app.core.auth import get_current_company

router = APIRouter()


@router.post("/customers/")
async def create_customer(
    customer: CustomerCreate,
    current_company: dict = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    db_customer = Customer(
        company_id=current_company["company_id"],
        customer_name=customer.customer_name,
        phone=customer.phone,
        email=customer.email,
        address_line_1=customer.address_line_1,
        address_line_2=customer.address_line_2,
        city=customer.city,
        state=customer.state,
        postal_code=customer.postal_code,
        country=customer.country,
        gst_number=customer.gst_number,
    )

    customer_service = CustomerService()

    saved_customer = customer_service.create_customer(db, db_customer)

    return {
        "message": "Customer created successfully",
        "data": saved_customer
    }


@router.get("/customers/")
async def get_all_customers(
    db: Session = Depends(get_db),
    current_company: dict = Depends(get_current_company)
):
    
    customer_service = CustomerService()
  
    customers = customer_service.get_all_customers(db=db, company_id=current_company["company_id"])

    return {
        "message": "Customers retrieved successfully",
        "data": customers
    }


@router.get("/customers/{customer_id}")
async def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer_service = CustomerService()

    customer = customer_service.get_customer_by_id(db, customer_id)

    if not customer:
        return {"message": "Customer not found"}

    return {
        "message": "Customer retrieved successfully",
        "data": customer
    }
