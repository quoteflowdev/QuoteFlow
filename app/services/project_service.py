from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.project import Project
from app.repositories.customer_repository import CustomerRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import (ProjectCreate, ProjectUpdate,)


class ProjectService:

    def __init__(self):
        self.project_repository = ProjectRepository()
        self.customer_repository = CustomerRepository()

    def _generate_project_code(
        self,
        db: Session,
    ) -> str:

        last_project = self.project_repository.get_last_project(db)

        if last_project is None:
            return "PRJ000001"

        next_number = last_project.id + 1

        return f"PRJ{next_number:06d}"

    def _generate_project_name(
        self,
        customer: Customer,
        site_address: str,
    ) -> str:

        city = site_address.split(",")[0].strip()

        return f"{customer.customer_name} - {city}"

    def create_project(
        self,
        db: Session,
        company_id: int,
        project_data: ProjectCreate,
    ) -> Project | None:

        customer = self.customer_repository.get_customer_by_id(
            db,
            company_id,
            project_data.customer_id,
        )

        if customer is None:
            return None

        project_name = project_data.project_name

        if not project_name:
            project_name = self._generate_project_name(
                customer,
                project_data.site_address,
            )

        project = Project(
            company_id=company_id,
            customer_id=project_data.customer_id,
            project_code=self._generate_project_code(db),
            project_name=project_name,
            site_address=project_data.site_address,
            created_by=company_id,
            updated_by=company_id,
        )

        return self.project_repository.create_project(
            db,
            project,
        )

    def get_all_projects(
        self,
        db: Session,
        company_id: int,
    ) -> list[Project]:

        return self.project_repository.get_projects(
            db,
            company_id,
        )

    def get_project_by_id(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ) -> Project | None:

        return self.project_repository.get_project_by_id(
            db,
            company_id,
            project_id,
        )

    def search_projects(
        self,
        db: Session,
        company_id: int,
        search: str,
    ) -> list[Project]:

        return self.project_repository.search_projects(
            db,
            company_id,
            search,
        )

    def update_project(
        self,
        db: Session,
        company_id: int,
        project_id: int,
        project_update: ProjectUpdate,
    ) -> Project | None:

        project = self.project_repository.get_project_by_id(
            db,
            company_id,
            project_id,
        )

        if project is None:
            return None

        update_data = project_update.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                project,
                field,
                value,
            )

        project.updated_by = company_id
        project.version += 1

        return self.project_repository.update_project(
            db,
            project,
        )

    def deactivate_project(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ) -> Project | None:

        project = self.project_repository.get_project_by_id(
            db,
            company_id,
            project_id,
        )

        if project is None:
            return None

        project.updated_by = company_id
        project.version += 1

        return self.project_repository.deactivate_project(
            db,
            project,
        )

    def restore_project(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ) -> Project | None:

        project = self.project_repository.get_project_by_id_any_status(
            db,
            company_id,
            project_id,
        )

        if project is None:
            return None

        project.updated_by = company_id
        project.version += 1

        return self.project_repository.restore_project(
            db,
            project,
        )