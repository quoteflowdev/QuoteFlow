from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import (CustomerCreate, CustomerUpdate)


class CustomerService:

    def __init__(self):
        self.customer_repository = CustomerRepository()

    def _generate_customer_code(
        self,
        db: Session
    ) -> str:

        last_customer = self.customer_repository.get_last_customer(db)

        if last_customer is None:
            return "CUS000001"

        return f"CUS{last_customer.id + 1:06d}"

    def create_customer(
        self,
        db: Session,
        company_id: int,
        customer_data: CustomerCreate
    ) -> Customer | None:

        if self.customer_repository.get_customer_by_phone(
            db,
            company_id,
            customer_data.phone,
        ):
            return None

        if (
            customer_data.email
            and self.customer_repository.get_customer_by_email(
                db,
                company_id,
                customer_data.email,
            )
        ):
            return None

        customer = Customer(
            company_id=company_id,
            customer_code=self._generate_customer_code(db),
            customer_name=customer_data.customer_name,
            phone=customer_data.phone,
            email=customer_data.email,
            address_line_1=customer_data.address_line_1,
            address_line_2=customer_data.address_line_2,
            city=customer_data.city,
            state=customer_data.state,
            postal_code=customer_data.postal_code,
            country=customer_data.country,
            gst_number=customer_data.gst_number,
            notes=customer_data.notes,
            created_by=company_id,
            updated_by=company_id,
        )

        return self.customer_repository.create_customer(
            db,
            customer,
        )

    def get_all_customers(
        self,
        db: Session,
        company_id: int
    ) -> list[Customer]:

        return self.customer_repository.get_customers(
            db,
            company_id,
        )

    def search_customers(
        self,
        db: Session,
        company_id: int,
        search: str,
        page: int = 1,
        limit: int = 20,
    ) -> list[Customer]:

        return self.customer_repository.search_customers(
            db=db,
            company_id=company_id,
            search=search,
            skip=(page - 1) * limit,
            limit=limit,
        )

    def get_customer_by_id(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
    ) -> Customer | None:

        return self.customer_repository.get_customer_by_id(
            db,
            company_id,
            customer_id,
        )

    def update_customer(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
        customer_update: CustomerUpdate,
    ) -> Customer | None:

        customer = self.customer_repository.get_customer_by_id(
            db,
            company_id,
            customer_id,
        )

        if customer is None:
            return None

        if (
            customer_update.phone
            and customer.phone != customer_update.phone
        ):
            if self.customer_repository.get_customer_by_phone(
                db,
                company_id,
                customer_update.phone,
            ):
                return None

        if (
            customer_update.email
            and customer.email != customer_update.email
        ):
            existing_customer = self.customer_repository.get_customer_by_email(
                db,
                company_id,
                customer_update.email,
            )

            if (
                existing_customer
                and existing_customer.id != customer.id
            ):
                return None

        update_data = customer_update.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                customer,
                field,
                value,
            )

        customer.updated_by = company_id
        customer.version += 1

        return self.customer_repository.update_customer(
            db,
            customer,
        )

    def deactivate_customer(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
    ) -> Customer | None:

        customer = self.customer_repository.get_customer_by_id(
            db,
            company_id,
            customer_id,
        )

        if customer is None:
            return None

        customer.updated_by = company_id
        customer.version += 1

        return self.customer_repository.deactivate_customer(
            db,
            customer,
        )

    def restore_customer(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
    ) -> Customer | None:

        customer = self.customer_repository.get_customer_by_id_any_status(
            db,
            company_id,
            customer_id
        )

        if customer is None:
            return None

        customer.updated_by = company_id
        customer.version += 1

        return self.customer_repository.restore_customer(
            db,
            customer,
        )