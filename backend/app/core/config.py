from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    HF_TOKEN: str
    GEMINI_API_KEY: str

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # App
    FRONTEND_URL: str = "http://localhost:3000"
    DOCS_FOLDER: str = "data/documents"

    # Embedding
    EMBEDDING_MODEL: str

    # Chunking
    CHUNK_SIZE: int = 900
    CHUNK_OVERLAP: int = 200

    # Retrieval
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.8

    # Gemini
    GEMINI_MODEL: str

    class Config:
        env_file = ".env"

settings = Settings()
