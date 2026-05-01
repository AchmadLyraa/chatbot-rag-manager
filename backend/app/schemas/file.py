from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    filename: str
    originalFilename: str
    storagePath: str
    mimeType: Optional[str] = None
    size: Optional[int] = None


class FileCreate(BaseModel):
    filename: str
    folderId: Optional[str] = None
    mimeType: Optional[str] = None
    size: Optional[int] = None


class FileSchema(FileBase):
    id: str
    folderId: Optional[str] = None
    indexed: bool = False
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
