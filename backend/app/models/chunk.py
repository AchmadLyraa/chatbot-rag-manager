from sqlalchemy import Column, Integer, Text, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.models.base import Base

class Chunk(Base):
    __tablename__ = "rag_chunks"

    id = Column(Integer, primary_key=True)
    file_id = Column(String(36), ForeignKey("file.id", ondelete="CASCADE"))

    content = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    embedding = Column(Vector(1024))

    file = relationship("File", back_populates="chunks")
