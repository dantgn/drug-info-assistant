from fastapi import FastAPI
from app.routers import drug_router

app = FastAPI(title="AI Drug Information Assistant")

app.include_router(drug_router.router, prefix="/api", tags=["Drug"])
