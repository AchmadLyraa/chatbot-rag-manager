from fastapi import APIRouter, UploadFile, File
from app.services.ingestion_service import run_ingestion
import shutil
import os

from app.core.config import settings


router = APIRouter()

UPLOAD_FOLDER = settings.DOCS_FOLDER

@router.post("/ingest")
async def ingest_documents():
    result = run_ingestion(UPLOAD_FOLDER)
    return result

@router.post("/ingest/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"status": "uploaded", "filename": file.filename}
