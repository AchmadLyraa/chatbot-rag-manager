from sqlalchemy import Column, Integer, String, JSON, Text
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class RagChunk(Base):
    __tablename__ = "rag_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=False)
    embedding = Column(Vector(1024), nullable=False)
