from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_company
from app.database.connection import get_db

from app.models.company import Company

from app.schemas.measurement import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementResponse,
    MeasurementDetailsResponse,
    MeasurementItemCreate,
    MeasurementItemUpdate,
    MeasurementItemResponse,
)

from app.services.measurement_service import MeasurementService


router = APIRouter()

measurement_service = MeasurementService()


# =====================================================
# Measurement
# =====================================================

@router.post(
    "/measurements/",
    response_model=MeasurementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_measurement(
    request: MeasurementCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    try:

        return measurement_service.create_measurement(
            db,
            current_company.id,
            request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/projects/{project_id}/measurements",
    response_model=list[MeasurementResponse],
)
async def get_project_measurements(
    project_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return measurement_service.get_measurements_by_project(
        db,
        current_company.id,
        project_id,
    )


@router.get(
    "/measurements/{measurement_id}",
    response_model=MeasurementDetailsResponse,
)
async def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    measurement = measurement_service.get_measurement_details(
        db,
        current_company.id,
        measurement_id,
    )

    if measurement is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found.",
        )

    return measurement


@router.put(
    "/measurements/{measurement_id}",
    response_model=MeasurementResponse,
)
async def update_measurement(
    measurement_id: int,
    request: MeasurementUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    measurement = measurement_service.update_measurement(
        db,
        current_company.id,
        measurement_id,
        request,
    )

    if measurement is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found.",
        )

    return measurement


@router.patch(
    "/measurements/{measurement_id}/deactivate",
)
async def deactivate_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    measurement = measurement_service.change_measurement_status(
        db,
        current_company.id,
        measurement_id,
        False,
    )

    if measurement is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found.",
        )

    return {
        "message": "Measurement deactivated successfully."
    }


@router.patch(
    "/measurements/{measurement_id}/restore",
)
async def restore_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    measurement = measurement_service.change_measurement_status(
        db,
        current_company.id,
        measurement_id,
        True,
    )

    if measurement is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found.",
        )

    return {
        "message": "Measurement restored successfully."
    }


# =====================================================
# Measurement Items
# =====================================================

@router.post(
    "/measurements/{measurement_id}/items",
    response_model=MeasurementItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_measurement_item(
    measurement_id: int,
    request: MeasurementItemCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    try:

        return measurement_service.add_measurement_item(
            db,
            current_company.id,
            measurement_id,
            request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get(
    "/measurements/{measurement_id}/items",
    response_model=list[MeasurementItemResponse],
)
async def get_measurement_items(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    items = measurement_service.get_measurement_items(
        db,
        current_company.id,
        measurement_id,
    )

    if items is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found.",
        )

    return items

@router.put(
    "/measurement-items/{item_id}",
    response_model=MeasurementItemResponse,
)
async def update_measurement_item(
    item_id: int,
    request: MeasurementItemUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    item = measurement_service.update_measurement_item(
        db,
        current_company.id,
        item_id,
        request,
    )

    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement item not found.",
        )

    return item


@router.patch(
    "/measurement-items/{item_id}/deactivate",
)
async def deactivate_measurement_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    item = measurement_service.change_measurement_item_status(
        db,
        current_company.id,
        item_id,
        False,
    )

    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement item not found.",
        )

    return {
        "message": "Measurement item deactivated successfully."
    }


@router.patch(
    "/measurement-items/{item_id}/restore",
)
async def restore_measurement_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    item = measurement_service.change_measurement_item_status(
        db,
        current_company.id,
        item_id,
        True,
    )

    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement item not found.",
        )

    return {
        "message": "Measurement item restored successfully."
    }