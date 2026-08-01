from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:

    def create_company(
        self,
        db: Session,
        company: Company
    ) -> Company:

        try:
            db.add(company)
            db.commit()
            db.refresh(company)

            return company

        except Exception:
            db.rollback()
            raise

    def get_companies(
        self,
        db: Session
    ) -> list[Company]:

        return (
            db.query(Company)
            .all()
        )

    def get_company_by_id(
        self,
        db: Session,
        company_id: int
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(Company.id == company_id)
            .first()
        )

    def update_company(
        self,
        db: Session,
        company: Company
    ) -> Company:

        try:
            db.commit()
            db.refresh(company)

            return company

        except Exception:
            db.rollback()
            raise

    def deactivate_company(
        self,
        db: Session,
        company: Company
    ) -> Company:

        company.status = "INACTIVE"

        try:
            db.commit()
            db.refresh(company)

            return company

        except Exception:
            db.rollback()
            raise