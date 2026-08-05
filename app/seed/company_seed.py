from sqlalchemy.orm import Session
from app.core.security import hash_password

from app.models.company import Company


def seed_company(db: Session):

    company = (
        db.query(Company)
        .filter(
            Company.email == "vision@gmail.com",
        )
        .first()
    )

    if company:
        return

    company = Company(
        company_name="Vision Aluminium",
        owner_name="Kuldeep Rajput",
        email="vision@gmail.com",
        phone_number="9028241196",
        business_type="Aluminium & Glass",
        company_address="Pune, Maharashtra",
        gst_number="27ABCDE1234F1Z5",
        password=hash_password("kuldeep@1"),
        status="ACTIVE",
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    print("✅ Company Seeded")