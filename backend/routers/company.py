from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Company, User
from auth import get_current_user


router = APIRouter(
    prefix="/company",
    tags=["Empresa"]
)


class CompanyRequest(BaseModel):
    name: str
    sector: str | None = None
    size: str | None = None
    description: str | None = None
    goal: str | None = None


@router.post("/")
def create_company(
    data: CompanyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_company = db.query(Company).filter(
        Company.user_id == current_user.id
    ).first()

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Este usuário já possui uma empresa cadastrada."
        )

    company = Company(
        name=data.name,
        sector=data.sector,
        size=data.size,
        description=data.description,
        goal=data.goal,
        user_id=current_user.id
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return {
        "message": "Empresa cadastrada com sucesso.",
        "company": {
            "id": company.id,
            "name": company.name,
            "sector": company.sector,
            "size": company.size,
            "description": company.description,
            "goal": company.goal
        }
    }


@router.get("/")
def get_company(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.user_id == current_user.id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma empresa cadastrada."
        )

    return {
        "id": company.id,
        "name": company.name,
        "sector": company.sector,
        "size": company.size,
        "description": company.description,
        "goal": company.goal
    }