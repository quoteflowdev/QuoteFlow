from fastapi import FastAPI

from app.api import customer
from app.api.company_router import router as company_router
from app.database.base import Base
from app.database.connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QuoteFlow API",
    description="Measurement and Quotation SaaS Platform",
    version="1.0.0"
)

app.include_router(
    company_router,
    prefix="/api/v1",
    tags=["Company"]
)

app.include_router(
    customer.router,
    prefix="/api/v1",
    tags=["Customer"]
)


@app.get("/")
async def root():

    return {
        "message": "Welcome to QuoteFlow API 🚀"
    }