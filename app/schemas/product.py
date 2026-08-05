from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    CalculationType,
    Status,
    Unit,
)


class ProductBase(BaseModel):
    product_name: str
    calculation_type: CalculationType
    default_unit: Unit
    allow_decimal: bool = True
    display_order: int = 0
    icon: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    calculation_type: Optional[CalculationType] = None
    default_unit: Optional[Unit] = None
    allow_decimal: Optional[bool] = None
    description: Optional[str] = None
    status: Optional[Status] = None


class ProductResponse(ProductBase):
    id: int
    company_id: Optional[int] = None
    product_code: str
    is_system: bool
    status: Status
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )