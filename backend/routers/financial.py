import os
import uuid

import pandas as pd

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from database import get_db
from models import Company, FinancialFile, User
from auth import get_current_user

from services.spreadsheet_analyzer import analyze_spreadsheet
from services.metrics_engine import calculate_metrics
from services.intelligence import generate_intelligence

router = APIRouter(
    prefix="/financial",
    tags=["Financeiro"]
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".xlsx",
    ".xls",
    ".csv"
}


@router.post("/upload")
def upload_financial_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.user_id == current_user.id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma empresa cadastrada para este usuário."
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Formato não permitido. Envie XLSX, XLS ou CSV."
        )

    unique_name = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    financial_file = FinancialFile(
        filename=file.filename,
        file_path=file_path,
        company_id=company.id
    )

    db.add(financial_file)
    db.commit()
    db.refresh(financial_file)

    return {
        "message": "Planilha financeira enviada com sucesso.",
        "file": {
            "id": financial_file.id,
            "filename": financial_file.filename,
            "company_id": financial_file.company_id
        }
    }


@router.get("/files")
def list_financial_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.user_id == current_user.id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma empresa cadastrada para este usuário."
        )

    files = db.query(FinancialFile).filter(
        FinancialFile.company_id == company.id
    ).order_by(
        FinancialFile.created_at.desc()
    ).all()

    return {
        "company_id": company.id,
        "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "created_at": file.created_at
            }
            for file in files
        ]
    }


@router.post("/analyze/{file_id}")
def analyze_financial_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.user_id == current_user.id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma empresa cadastrada para este usuário."
        )

    financial_file = db.query(FinancialFile).filter(
        FinancialFile.id == file_id,
        FinancialFile.company_id == company.id
    ).first()

    if not financial_file:
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado."
        )

    file_path = financial_file.file_path

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Arquivo físico não encontrado."
        )

    try:
        extension = os.path.splitext(
            financial_file.filename
        )[1].lower()

        if extension == ".csv":
            dataframe = pd.read_csv(
                file_path
            )
        else:
            dataframe = pd.read_excel(
                file_path,
                header=None
            )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Não foi possível ler a planilha: "
                f"{str(error)}"
            )
        )

    analysis = analyze_spreadsheet(
        dataframe
    )

    metrics = calculate_metrics(
        dataframe
    )

    analysis["metrics"] = metrics

    intelligence = generate_intelligence(
        analysis
    )

    return {
        "message": "Planilha analisada com sucesso.",
        "company_id": company.id,
        "file": financial_file.filename,
        "analysis": analysis,
        "intelligence": intelligence
    }