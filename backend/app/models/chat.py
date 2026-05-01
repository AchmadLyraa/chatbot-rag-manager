from pydantic import BaseModel
from typing import Literal


class MessageSchema(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[MessageSchema]
