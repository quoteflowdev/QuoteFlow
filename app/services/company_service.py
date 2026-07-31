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

    def update_company(self, db, company_id, company_update):
        company_repository = CompanyRepository()

        company = company_repository.get_company_by_id(db, company_id)

        if not company:
            return None

        if company_update.company_name is not None:
            company.company_name = company_update.company_name

        if company_update.owner_name is not None:
            company.owner_name = company_update.owner_name

        if company_update.business_type is not None:
            company.business_type = company_update.business_type

        if company_update.company_address is not None:
            company.company_address = company_update.company_address

        if company_update.gst_number is not None:
            company.gst_number = company_update.gst_number

        return company_repository.update_company(db, company)