from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.models.chunk import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, done, failed
    uploaded_at = Column(DateTime, server_default=func.now())
    processed_at = Column(DateTime, nullable=True)
    chunk_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
