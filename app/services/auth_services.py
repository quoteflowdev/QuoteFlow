from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.company import Company
from app.repositories.auth_repository import AuthRepository


class AuthService:

    def __init__(self):
        self.auth_repository = AuthRepository()

    def authenticate_company(
        self,
        db: Session,
        phone_number: str,
        password: str
    ) -> Company | None:

        company = self.auth_repository.get_active_company_by_phone(
            db,
            phone_number
        )

        if company is None:
            return None

        if not verify_password(
            password,
            company.password
        ):
            return None

        return company

    def get_current_company(
        self,
        db: Session,
        company_id: int
    ) -> Company | None:

        return self.auth_repository.get_active_company_by_id(
            db,
            company_id
        )