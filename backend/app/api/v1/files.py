from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.file import FileSchema, FileCreate, APIResponse
from app.services.file_service import FileService
from typing import List, Optional
from app.services.ingestion_service import run_ingestion
from app.core.config import settings
import os

router = APIRouter()

@router.get("/files", response_model=List[FileSchema])
async def get_files(folderId: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        return FileService.get_files(db, folderId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/files/{file_id}", response_model=FileSchema)
async def get_file(file_id: str, db: Session = Depends(get_db)):
    try:
        file = FileService.get_file_by_id(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        return file
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/files", response_model=FileSchema)
async def create_file(file_data: FileCreate, db: Session = Depends(get_db)):
    try:
        return FileService.create_file(
            db,
            file_data.filename,
            file_data.folderId,
            file_data.mimeType,
            file_data.size
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create file")


@router.post("/files/upload", response_model=FileSchema)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    folderId: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()

        original_filename = file.filename

        uuid_filename, storage_path = FileService.save_file_content(
            original_filename,
            content
        )

        created_file = FileService.create_file_with_path(
            db,
            original_filename,
            uuid_filename,
            storage_path,
            folderId,
            mimeType=file.content_type,
            size=len(content)
        )

        return created_file

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{file_id}", response_model=APIResponse)
async def delete_file(file_id: str, db: Session = Depends(get_db)):
    try:
        success = FileService.delete_file(db, file_id)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete file")

@router.post("/files/{file_id}/index", response_model=APIResponse)
async def index_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    try:
        file = FileService.get_file_by_id(db, file_id)

        if not file:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        if file.indexed:
            raise HTTPException(
                status_code=400,
                detail="File already indexed"
            )
        if file.mimeType not in ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(
                status_code=400,
                detail="File type not supported for indexing"
            )

        file_path = os.path.join(
            settings.STORAGE_BASE_PATH,
            file.filename
        )

        run_ingestion(file.id, file_path)

        file.indexed = True

        db.commit()
        db.refresh(file)

        return {
            "success": True
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
