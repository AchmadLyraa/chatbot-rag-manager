from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.file import FileSchema, FileCreate, APIResponse
from app.services.file_service import FileService
from typing import List, Optional

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
    filename: str = Form(...),
    folderId: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()
        uuid_filename, storage_path = FileService.save_file_content(filename, content)
        return FileService.create_file_with_path(
            db,
            filename,
            uuid_filename,
            storage_path,
            folderId,
            mimeType=file.content_type,
            size=len(content)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
