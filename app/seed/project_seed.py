from sqlalchemy.orm import Session

from app.core.enums import (
    ProjectStatus,
    Status,
)
from app.models.company import Company
from app.models.customer import Customer
from app.models.project import Project


def seed_projects(db: Session):

    company = (
        db.query(Company)
        .filter(
            Company.email == "vision@gmail.com",
        )
        .first()
    )

    if company is None:
        return

    projects = [
        {
            "customer_code": "CUST000001",
            "project_code": "PRJ000001",
            "project_name": "Kharadi Villa",
            "site_address": "Kharadi, Pune",
        },
        {
            "customer_code": "CUST000001",
            "project_code": "PRJ000002",
            "project_name": "Baner Bungalow",
            "site_address": "Baner, Pune",
        },
        {
            "customer_code": "CUST000002",
            "project_code": "PRJ000003",
            "project_name": "Wagholi Residency",
            "site_address": "Wagholi, Pune",
        },
        {
            "customer_code": "CUST000003",
            "project_code": "PRJ000004",
            "project_name": "Office Interior",
            "site_address": "Hinjewadi, Pune",
        },
    ]

    for project_data in projects:

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_code == project_data["customer_code"],
            )
            .first()
        )

        if customer is None:
            continue

        exists = (
            db.query(Project)
            .filter(
                Project.project_code == project_data["project_code"],
            )
            .first()
        )

        if exists:
            continue

        project = Project(
            company_id=company.id,
            customer_id=customer.id,
            project_code=project_data["project_code"],
            project_name=project_data["project_name"],
            site_address=project_data["site_address"],
            site_contact_name=None,
            site_contact_number=None,
            remarks=None,
            project_status=ProjectStatus.NEW,
            status=Status.ACTIVE,
            created_by=None,
            updated_by=None,
            version=1,
        )

        db.add(project)

    db.commit()

    print("✅ Projects Seeded")