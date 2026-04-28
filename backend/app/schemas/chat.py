from pydantic import BaseModel
from typing import Literal

class MessageSchema(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    session_id: str
    messages: list[MessageSchema]

class ChatResponse(BaseModel):
    session_id: str
    answer: str
