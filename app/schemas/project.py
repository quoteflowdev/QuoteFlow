from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import Status


class ProjectBase(BaseModel):
    project_name: Optional[str] = None
    site_address: str


class ProjectCreate(ProjectBase):
    customer_id: int


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    site_address: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int

    company_id: int
    customer_id: int

    project_code: str

    project_name: str
    site_address: str
    status: Status

    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    version: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )