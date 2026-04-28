from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IngestResponse(BaseModel):
    status: str
    chunks_inserted: int

class UploadResponse(BaseModel):
    status: str
    filename: str

class DocumentSchema(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime
    processed_at: Optional[datetime]
    chunk_count: int
    error_message: Optional[str]

    class Config:
        from_attributes = True
