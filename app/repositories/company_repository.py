from sqlalchemy.orm import Session
from app.models.company import Company

class CompanyRepository:
    def create_company(
            self, 
            db: Session, 
            company: Company
    ):
        db.add(company)
        db.commit()
        db.refresh(company)

        return company

    def get_company(
            self,
            db
    ):
        return db.query(Company).all()

    def get_company_by_id(
            self,
            db: Session,
            company_id: int
    ):
        return db.query(Company).filter(Company.id == company_id).first()

    def get_company_by_email(
            self,
            db: Session,
            email: str
    ):
        return db.query(Company).filter(Company.email == email).first()