from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.file import FileSchema


class FolderBase(BaseModel):
    name: str
    parentId: Optional[str] = None


class FolderCreate(FolderBase):
    pass


class FolderSchema(FolderBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class FolderWithChildren(FolderSchema):
    children: List[FolderSchema] = Field(default_factory=list)
    files: List["FileSchema"] = Field(default_factory=list)


FolderWithChildren.model_rebuild()
