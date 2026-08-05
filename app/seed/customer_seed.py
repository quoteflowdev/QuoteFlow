from sqlalchemy.orm import Session

from app.core.enums import Status
from app.models.company import Company
from app.models.customer import Customer


def seed_customer(db: Session):

    company = (
        db.query(Company)
        .filter(
            Company.email == "vision@gmail.com",
        )
        .first()
    )

    if company is None:
        return

    customers = [
        {
            "customer_code": "CUST000001",
            "customer_name": "Rahul Patil",
            "phone": "9876543211",
            "email": "rahul@gmail.com",
            "address_line_1": "Kharadi",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411014",
        },
        {
            "customer_code": "CUST000002",
            "customer_name": "Sachin Shinde",
            "phone": "9876543212",
            "email": "sachin@gmail.com",
            "address_line_1": "Wagholi",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "412207",
        },
        {
            "customer_code": "CUST000003",
            "customer_name": "Amit Jadhav",
            "phone": "9876543213",
            "email": "amit@gmail.com",
            "address_line_1": "Baner",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411045",
        },
    ]

    for customer_data in customers:

        exists = (
            db.query(Customer)
            .filter(
                Customer.customer_code == customer_data["customer_code"],
            )
            .first()
        )

        if exists:
            continue

        customer = Customer(
            company_id=company.id,
            customer_code=customer_data["customer_code"],
            customer_name=customer_data["customer_name"],
            phone=customer_data["phone"],
            email=customer_data["email"],
            address_line_1=customer_data["address_line_1"],
            address_line_2=None,
            city=customer_data["city"],
            state=customer_data["state"],
            postal_code=customer_data["postal_code"],
            country="India",
            gst_number=None,
            notes=None,
            status=Status.ACTIVE,
            created_by=None,
            updated_by=None,
            version=1,
        )

        db.add(customer)

    db.commit()

    print("✅ Customers Seeded")