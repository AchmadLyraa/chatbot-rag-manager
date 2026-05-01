from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.models.base import Base


class File(Base):
    __tablename__ = "file"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    originalFilename = Column(String(255), nullable=False)
    storagePath = Column(String(500), nullable=False)
    mimeType = Column(String(100), nullable=True)
    size = Column(Integer, nullable=True)
    indexed = Column(Boolean, default=False)
    folderId = Column(String(36), ForeignKey("folder.id", ondelete="CASCADE"), nullable=True, index=True)

    folder = relationship("Folder", back_populates="files")

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
