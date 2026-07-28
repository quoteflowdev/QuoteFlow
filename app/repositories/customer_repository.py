from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:

    def create_customer(
        self,
        db: Session,
        customer: Customer
    ):
        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    def get_customers(
        self,
        db: Session
    ):
        return db.query(Customer).all()

    def get_customer_by_id(
        self,
        db: Session,
        customer_id: int
    ):
        return db.query(Customer).filter(Customer.id == customer_id).first()

    def update_customer(
        self,
        db: Session,
        customer: Customer
    ):
        db.commit()
        db.refresh(customer)

        return customer


    def delete_customer(
    self,
    db: Session,
    customer: Customer
    ):
        customer.is_active = False
        db.commit()
        db.refresh(customer)

        return customer

    def get_all_customers(self, db, company_id):
        return (
            db.query(Customer).filter(Customer.company_id == company_id, Customer.is_active == True).all()
        )
     

    