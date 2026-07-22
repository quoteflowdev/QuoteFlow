from fastapi import FastAPI
from app.api.company import router as company_router

app = FastAPI(
    title="QouteFlow API",
    description="Measurement and Quotation SaaS Platform for QouteFlow",
    version="1.0.0",
)

app.include_router(company_router)
@app.get("/")
async def root():
    return {"message": "Welcome to QouteFlow"}