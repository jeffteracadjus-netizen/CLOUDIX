from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import engine, Base
import models

from routers.auth import router as auth_router
from routers.company import router as company_router
from routers.financial import router as financial_router
from routers.ai import router as ai_router

# ==========================================================
# BANCO DE DADOS
# ==========================================================

Base.metadata.create_all(bind=engine)


# ==========================================================
# APLICAÇÃO CLOUDIX
# ==========================================================

app = FastAPI(
    title="CLOUDIX API",
    description="API da plataforma CLOUDIX AI",
    version="1.0.0"
)


# ==========================================================
# CONFIGURAÇÃO DE CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos os cabeçalhos (inclusive Authorization/JWT)
)


# ==========================================================
# ROTAS DA API
# ==========================================================

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(financial_router)
app.include_router(ai_router)


# ==========================================================
# FRONTEND
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "services" / "frontend"


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )