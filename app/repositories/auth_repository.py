from sqlalchemy.orm import Session

from app.models.company import Company


class AuthRepository:

    def get_company_by_email(
        self,
        db: Session,
        email: str
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(Company.email == email)
            .first()
        )

    def get_company_by_phone(
        self,
        db: Session,
        phone_number: str
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(Company.phone_number == phone_number)
            .first()
        )

    def get_active_company_by_email(
        self,
        db: Session,
        email: str
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(
                Company.email == email,
                Company.status == "ACTIVE"
            )
            .first()
        )

    def get_active_company_by_phone(
        self,
        db: Session,
        phone_number: str
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(
                Company.phone_number == phone_number,
                Company.status == "ACTIVE"
            )
            .first()
        )

    def get_active_company_by_id(
        self,
        db: Session,
        company_id: int
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(
                Company.id == company_id,
                Company.status == "ACTIVE"
            )
            .first()
        )