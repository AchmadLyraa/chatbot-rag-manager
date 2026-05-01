from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.folder import FolderSchema, FolderCreate, FolderWithChildren
from app.schemas.file import APIResponse
from app.services.folder_service import FolderService
from typing import List, Optional

router = APIRouter()


@router.get("/folders", response_model=List[FolderSchema])
async def get_folders(parentId: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        return FolderService.get_folders(db, parentId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/folders/{folder_id}", response_model=FolderSchema)
async def get_folder(folder_id: str, db: Session = Depends(get_db)):
    try:
        folder = FolderService.get_folder_by_id(db, folder_id)
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        return folder
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/folders", response_model=FolderSchema)
async def create_folder(payload: FolderCreate, db: Session = Depends(get_db)):
    try:
        return FolderService.create_folder(db, payload.name, payload.parentId)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/folders/{folder_id}", response_model=APIResponse)
async def delete_folder(folder_id: str, db: Session = Depends(get_db)):
    try:
        success = FolderService.delete_folder(db, folder_id)
        if not success:
            raise HTTPException(status_code=404, detail="Folder not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
