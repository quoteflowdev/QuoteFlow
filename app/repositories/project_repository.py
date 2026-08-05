from sqlalchemy.orm import Session

from app.core.enums import Status
from app.models.project import Project


class ProjectRepository:

    def create_project(
        self,
        db: Session,
        project: Project,
    ) -> Project:

        db.add(project)

        try:
            db.commit()
            db.refresh(project)
            return project

        except Exception:
            db.rollback()
            raise

    def get_projects(
        self,
        db: Session,
        company_id: int,
    ) -> list[Project]:

        return (
            db.query(Project)
            .filter(
                Project.company_id == company_id,
                Project.status == Status.ACTIVE,
            )
            .order_by(
                Project.id.desc()
            )
            .all()
        )

    def get_project_by_id(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ) -> Project | None:

        return (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.company_id == company_id,
                Project.status == Status.ACTIVE,
            )
            .first()
        )

    def get_project_by_id_any_status(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ) -> Project | None:

        return (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.company_id == company_id,
            )
            .first()
        )

    def search_projects(
        self,
        db: Session,
        company_id: int,
        search: str,
    ) -> list[Project]:

        return (
            db.query(Project)
            .filter(
                Project.company_id == company_id,
                Project.status == Status.ACTIVE,
                Project.project_name.ilike(f"%{search}%"),
            )
            .order_by(
                Project.id.desc()
            )
            .all()
        )

    def get_last_project(
        self,
        db: Session,
    ) -> Project | None:

        return (
            db.query(Project)
            .order_by(
                Project.id.desc()
            )
            .first()
        )

    def update_project(
        self,
        db: Session,
        project: Project,
    ) -> Project:

        try:
            db.commit()
            db.refresh(project)
            return project

        except Exception:
            db.rollback()
            raise

    def deactivate_project(
        self,
        db: Session,
        project: Project,
    ) -> Project:

        project.status = Status.INACTIVE

        try:
            db.commit()
            db.refresh(project)
            return project

        except Exception:
            db.rollback()
            raise

    def restore_project(
        self,
        db: Session,
        project: Project,
    ) -> Project:

        project.status = Status.ACTIVE

        try:
            db.commit()
            db.refresh(project)
            return project

        except Exception:
            db.rollback()
            raise