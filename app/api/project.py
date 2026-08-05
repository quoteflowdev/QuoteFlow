from fastapi import (APIRouter, Depends, HTTPException, Query, status,)
from sqlalchemy.orm import Session

from app.core.auth import get_current_company
from app.database.connection import get_db
from app.models.company import Company
from app.schemas.project import (ProjectCreate, ProjectResponse, ProjectUpdate,)
from app.services.project_service import ProjectService


router = APIRouter()

project_service = ProjectService()


@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED,)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    saved_project = project_service.create_project(
        db=db,
        company_id=current_company.id,
        project_data=project,
    )

    if saved_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return saved_project


@router.get("/projects/", response_model=list[ProjectResponse],)
async def get_all_projects(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return project_service.get_all_projects(
        db=db,
        company_id=current_company.id,
    )


@router.get("/projects/search/", response_model=list[ProjectResponse],)
async def search_projects(
    search: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    return project_service.search_projects(
        db=db,
        company_id=current_company.id,
        search=search,
    )


@router.get("/projects/{project_id}", response_model=ProjectResponse,)
async def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    project = project_service.get_project_by_id(
        db=db,
        company_id=current_company.id,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse,)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    project = project_service.update_project(
        db=db,
        company_id=current_company.id,
        project_id=project_id,
        project_update=project_update,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch("/projects/{project_id}/deactivate", response_model=ProjectResponse,)
async def deactivate_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    project = project_service.deactivate_project(
        db=db,
        company_id=current_company.id,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch("/projects/{project_id}/restore", response_model=ProjectResponse,)
async def restore_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):

    project = project_service.restore_project(
        db=db,
        company_id=current_company.id,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project