from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat, ingestion
from app.core.config import settings

app = FastAPI(title= "Chatbot with RAG Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(ingestion.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "ok"}
