from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.api.company import router as company_router
from app.api.customer import router as customer_router
from app.api.product import router as product_router
from app.api.project import router as project_router
from app.api.measurement import router as measurement_router


from app.database.base import Base
from app.database.connection import engine

from app.seed.company_seed import seed_company
from app.seed.customer_seed import seed_customer
from app.seed.project_seed import seed_projects
from app.seed.product_seed import seed_products

Base.metadata.create_all(bind=engine)

db = Session(bind=engine)
seed_company(db)
seed_customer(db)
seed_projects(db)
seed_products(db)
db.close()

app = FastAPI(
    title="MaapBook API",
    description="Measurement and Quotation SaaS Platform",
    version="1.0.0",
)

app.include_router(
    company_router,
    prefix="/api/v1",
    tags=["Company"],
)

app.include_router(
    customer_router,
    prefix="/api/v1",
    tags=["Customer"],
)

app.include_router(
    product_router,
    prefix="/api/v1",
    tags=["Product"],
)

app.include_router(
    project_router,
    prefix="/api/v1",
    tags=["Project"],
)

app.include_router(
    measurement_router,
    prefix="/api/v1",
    tags=["Measurement"],
)

@app.get("/")
async def root():

    return {
        "message": "Welcome to MaapBook API 🚀"
    }