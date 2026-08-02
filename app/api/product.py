from fastapi import (APIRouter, Depends, HTTPException, Query, status,)
from sqlalchemy.orm import Session

from app.core.auth import get_current_company
from app.database.connection import get_db
from app.models.company import Company
from app.schemas.product import (ProductCreate, ProductResponse, ProductUpdate,)
from app.services.product_service import ProductService


router = APIRouter()

product_service = ProductService()


@router.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    saved_product = product_service.create_product(
        db=db,
        company_id=current_company.id,
        product_data=product,
    )

    if saved_product is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists.",
        )

    return saved_product


@router.get(
    "/products/",
    response_model=list[ProductResponse],
)
async def get_all_products(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return product_service.get_all_products(
        db=db,
        company_id=current_company.id,
    )


@router.get(
    "/products/search/",
    response_model=list[ProductResponse],
)
async def search_products(
    search: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return product_service.search_products(
        db=db,
        company_id=current_company.id,
        search=search,
        page=page,
        limit=limit,
    )


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
)
async def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    product = product_service.get_product_by_id(
        db=db,
        company_id=current_company.id,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    product = product_service.update_product(
        db=db,
        company_id=current_company.id,
        product_id=product_id,
        product_update=product_update,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or cannot be updated.",
        )

    return product


@router.patch(
    "/products/{product_id}/deactivate",
    response_model=ProductResponse,
)
async def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    product = product_service.deactivate_product(
        db=db,
        company_id=current_company.id,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or cannot be deactivated.",
        )

    return product


@router.patch(
    "/products/{product_id}/restore",
    response_model=ProductResponse,
)
async def restore_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    product = product_service.restore_product(
        db=db,
        company_id=current_company.id,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or cannot be restored.",
        )

    return product