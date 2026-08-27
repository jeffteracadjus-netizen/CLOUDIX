from fastapi import FastAPI

from database import engine, Base
import models

from routers.auth import router as auth_router
from routers.company import router as company_router
from routers.financial import router as financial_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CLOUDIX API",
    description="API da plataforma CLOUDIX AI",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(company_router)
app.include_router(financial_router)


@app.get("/")
def home():
    return {
        "message": "CLOUDIX API está funcionando!"
    }