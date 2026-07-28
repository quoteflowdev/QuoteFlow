from app.repositories.company_repository import CompanyRepository
from app.core.security import hash_password
from app.core.security import verify_password

class CompanyService:
    def create_company(self, db, company):

        # Hash the company's password before saving
        company.password = hash_password(company.password)

        company_repository = CompanyRepository()

        saved_company = company_repository.create_company(db, company)

        return saved_company

    def get_all_companies(self, db):

        company_repository = CompanyRepository()

        companies = company_repository.get_company(db)

        return companies

    def get_company_by_id(self, db, company_id):

        company_repository = CompanyRepository()

        company = company_repository.get_company_by_id(db, company_id)

        return company

    def login_company(self, db, email, password):

        company_repository = CompanyRepository()

        company = company_repository.get_company_by_email(db, email)

        if not company:
            return None

        # Verify the password
        if not verify_password(password, company.password):
            return None

        return company