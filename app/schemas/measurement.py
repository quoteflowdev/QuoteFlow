from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Product Info
# =====================================================

class ProductInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    default_unit: str


# =====================================================
# Measurement Item
# =====================================================

class MeasurementItemCreate(BaseModel):

    location: str

    height_feet: Optional[int] = None
    height_inch: Optional[float] = 0

    width_feet: Optional[int] = None
    width_inch: Optional[float] = 0

    length_feet: Optional[int] = None
    length_inch: Optional[float] = 0

    quantity: int = 1

    remarks: Optional[str] = None


class MeasurementItemUpdate(BaseModel):

    location: Optional[str] = None

    height_feet: Optional[int] = None
    height_inch: Optional[float] = None

    width_feet: Optional[int] = None
    width_inch: Optional[float] = None

    length_feet: Optional[int] = None
    length_inch: Optional[float] = None

    quantity: Optional[int] = None

    remarks: Optional[str] = None


class MeasurementItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    location: str

    height_feet: Optional[int]
    height_inch: Optional[float]

    width_feet: Optional[int]
    width_inch: Optional[float]

    length_feet: Optional[int]
    length_inch: Optional[float]

    quantity: int

    unit_value: float

    calculated_value: float

    remarks: Optional[str]

    created_at: datetime


# =====================================================
# Measurement
# =====================================================

class MeasurementCreate(BaseModel):

    project_id: int

    product_id: int

    measurement_name: str


class MeasurementUpdate(BaseModel):

    measurement_name: Optional[str] = None


class MeasurementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    measurement_code: str

    measurement_name: str

    project_id: int

    product: ProductInfo

    created_at: datetime


class MeasurementDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    measurement_code: str

    measurement_name: str

    project_id: int

    product: ProductInfo

    items: list[MeasurementItemResponse]

    created_at: datetime