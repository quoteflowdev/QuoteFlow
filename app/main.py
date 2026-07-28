from fastapi import FastAPI
from app.api.company import router as company_router
from app.api import customer
from app.database.connection import engine
from app.database.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QouteFlow API",
    description="Measurement and Quotation SaaS Platform for QouteFlow",
    version="1.0.0",
)

app.include_router(company_router)
app.include_router(customer.router)
@app.get("/")
async def root():
    return {"message": "Welcome to QouteFlow"}