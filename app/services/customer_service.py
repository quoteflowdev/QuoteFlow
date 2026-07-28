from app.repositories.customer_repository import CustomerRepository


class CustomerService:

    def create_customer(self, db, customer):

        customer_repository = CustomerRepository()

        saved_customer = customer_repository.create_customer(db, customer)

        return saved_customer

    def get_all_customers(self, db, company_id):

        customer_repository = CustomerRepository()

        return customer_repository.get_all_customers(db=db, company_id = company_id)

    def get_customer_by_id(self, db, customer_id):

        customer_repository = CustomerRepository()

        return customer_repository.get_customer_by_id(db, customer_id)

    def update_customer(self, db, customer):

        customer_repository = CustomerRepository()

        return customer_repository.update_customer(db, customer)

    def delete_customer(self, db, customer):

        customer_repository = CustomerRepository()

        return customer_repository.delete_customer(db, customer)