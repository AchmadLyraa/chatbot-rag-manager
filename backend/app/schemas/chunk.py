from pydantic import BaseModel
from typing import Optional

class ChunkSchema(BaseModel):
    id: int
    content: str
    metadata: dict
    score: Optional[float] = None

    class Config:
        from_attributes = True
