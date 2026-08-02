from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.company import Company
from app.repositories.auth_repository import AuthRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import (CompanyCreate, CompanyUpdate)


class CompanyService:

    def __init__(self):
        self.company_repository = CompanyRepository()
        self.auth_repository = AuthRepository()

    def create_company(
        self,
        db: Session,
        company_data: CompanyCreate
    ) -> Company:

        if self.auth_repository.get_company_by_email(
            db,
            company_data.email
        ):
            raise ValueError("Email already registered.")

        if self.auth_repository.get_company_by_phone(
            db,
            company_data.phone_number
        ):
            raise ValueError("Phone number already registered.")

        existing_gst = (
            db.query(Company)
            .filter(
                Company.gst_number == company_data.gst_number
            )
            .first()
        )

        if existing_gst:
            raise ValueError("GST number already registered.")

        company = Company(
            company_name=company_data.company_name,
            owner_name=company_data.owner_name,
            email=company_data.email,
            phone_number=company_data.phone_number,
            business_type=company_data.business_type,
            company_address=company_data.company_address,
            gst_number=company_data.gst_number,
            password=hash_password(company_data.password)
        )

        return self.company_repository.create_company(
            db,
            company
        )

    def get_all_companies(
        self,
        db: Session
    ) -> list[Company]:

        return self.company_repository.get_companies(db)

    def get_company_by_id(
        self,
        db: Session,
        company_id: int
    ) -> Company | None:

        return self.company_repository.get_company_by_id(
            db,
            company_id
        )

    def update_company(
        self,
        db: Session,
        company_id: int,
        company_update: CompanyUpdate
    ) -> Company | None:

        company = self.company_repository.get_company_by_id(
            db,
            company_id
        )

        if company is None:
            return None

        update_data = company_update.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        for field, value in update_data.items():
            setattr(
                company,
                field,
                value
            )

        return self.company_repository.update_company(
            db,
            company
        )

    def deactivate_company(
        self,
        db: Session,
        company_id: int
    ) -> Company | None:

        company = self.company_repository.get_company_by_id(
            db,
            company_id
        )

        if company is None:
            return None

        return self.company_repository.deactivate_company(
            db,
            company
        )