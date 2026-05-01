from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import chat, ingestion, files, folders
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models.folder import Folder
from app.models.file import File
import os

# Auto-create tables
Base.metadata.create_all(bind=engine)

# Create storage folder if not exists
os.makedirs(settings.STORAGE_BASE_PATH, exist_ok=True)

app = FastAPI(title="PLN RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving untuk download/preview file
app.mount("/files", StaticFiles(directory=settings.STORAGE_BASE_PATH), name="files")

app.include_router(chat.router, prefix="/api/v1")
app.include_router(ingestion.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1", tags=["files"])
app.include_router(folders.router, prefix="/api/v1", tags=["folders"])


@app.get("/")
def root():
    return {"status": "ok"}
