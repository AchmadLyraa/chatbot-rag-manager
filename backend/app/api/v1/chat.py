from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.chat_service import chat_stream

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@router.post("/chat")
async def chat(request: ChatRequest):
    messages = [m.model_dump() for m in request.messages]

    if not messages or not messages[-1]["content"]:
        return {"error": "No query provided"}

    return StreamingResponse(
        chat_stream(messages),
        media_type="text/event-stream"
    )
