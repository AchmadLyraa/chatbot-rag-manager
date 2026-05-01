from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.models.base import Base


class Folder(Base):
    __tablename__ = "folder"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    parentId = Column(String(36), ForeignKey("folder.id", ondelete="CASCADE"), nullable=True, index=True)

    parent = relationship("Folder", remote_side=[id], backref="children", foreign_keys=[parentId])
    files = relationship("File", back_populates="folder", cascade="all, delete-orphan")

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
