from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:

    def create_customer(
        self,
        db: Session,
        customer: Customer
    ) -> Customer:

        db.add(customer)

        try:
            db.commit()
            db.refresh(customer)
            return customer

        except Exception:
            db.rollback()
            raise

    def get_customers(
        self,
        db: Session,
        company_id: int
    ) -> list[Customer]:

        return (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.status == "ACTIVE"
            )
            .order_by(Customer.customer_name.asc())
            .all()
        )

    def search_customers(
        self,
        db: Session,
        company_id: int,
        search: str,
        skip: int = 0,
        limit: int = 20
    ) -> list[Customer]:

        return (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.status == "ACTIVE",
                or_(
                    Customer.customer_name.ilike(f"%{search}%"),
                    Customer.phone.ilike(f"%{search}%"),
                    Customer.customer_code.ilike(f"%{search}%"),
                    Customer.email.ilike(f"%{search}%")
                )
            )
            .order_by(Customer.customer_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_customer_by_id(
        self,
        db: Session,
        company_id: int,
        customer_id: int
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.company_id == company_id,
                Customer.status == "ACTIVE"
            )
            .first()
        )
    def get_customer_by_id_any_status(
        self,
        db: Session,
        company_id: int,
        customer_id: int
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.company_id == company_id
            )
            .first()
        )

    def get_customer_by_phone(
        self,
        db: Session,
        company_id: int,
        phone: str
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.phone == phone,
                Customer.status == "ACTIVE"
            )
            .first()
        )

    def get_customer_by_email(
        self,
        db: Session,
        company_id: int,
        email: str
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.email == email,
                Customer.status == "ACTIVE"
            )
            .first()
        )

    def get_customer_by_code(
        self,
        db: Session,
        company_id: int,
        customer_code: str
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.customer_code == customer_code,
                Customer.status == "ACTIVE"
            )
            .first()
        )

    def get_last_customer(
        self,
        db: Session
    ) -> Customer | None:

        return (
            db.query(Customer)
            .order_by(Customer.id.desc())
            .first()
        )

    def update_customer(
        self,
        db: Session,
        customer: Customer
    ) -> Customer:

        try:
            db.commit()
            db.refresh(customer)
            return customer

        except Exception:
            db.rollback()
            raise

    def deactivate_customer(
        self,
        db: Session,
        customer: Customer
    ) -> Customer:

        customer.status = "INACTIVE"

        try:
            db.commit()
            db.refresh(customer)
            return customer

        except Exception:
            db.rollback()
            raise

    def restore_customer(
        self,
        db: Session,
        customer: Customer
    ) -> Customer:

        customer.status = "ACTIVE"

        try:
            db.commit()
            db.refresh(customer)
            return customer

        except Exception:
            db.rollback()
            raise