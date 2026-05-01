from sqlalchemy.orm import Session
from app.models.file import File
from app.core.config import settings
from typing import List, Optional
import os
import uuid
from pathlib import Path


class FileService:
    @staticmethod
    def get_files(db: Session, folderId: Optional[str] = None) -> List[File]:
        query = db.query(File)
        if folderId and folderId != "root":
            query = query.filter(File.folderId == folderId)
        else:
            query = query.filter(File.folderId == None)
        return query.order_by(File.filename).all()

    @staticmethod
    def get_file_by_id(db: Session, file_id: str) -> Optional[File]:
        return db.query(File).filter(File.id == file_id).first()

    @staticmethod
    def create_file(
        db: Session,
        filename: str,
        folderId: Optional[str] = None,
        mimeType: Optional[str] = None,
        size: Optional[int] = None,
    ) -> File:
        if not filename or not filename.strip():
            raise ValueError("Filename is required")

        trimmed_filename = filename.strip()
        actual_folder_id = None if (folderId == "root" or not folderId) else folderId

        file_ext = Path(trimmed_filename).suffix
        uuid_filename = f"{uuid.uuid4()}{file_ext}"

        file = File(
            filename=uuid_filename,
            originalFilename=trimmed_filename,
            folderId=actual_folder_id,
            mimeType=mimeType,
            size=size,
            storagePath=f"/files/{uuid_filename}"
        )
        db.add(file)
        db.commit()
        db.refresh(file)
        return file

    @staticmethod
    def delete_file(db: Session, file_id: str) -> bool:
        if not file_id:
            raise ValueError("File ID is required")

        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            return False

        try:
            file_path = os.path.join(settings.STORAGE_BASE_PATH, file.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not delete physical file: {e}")

        db.delete(file)
        db.commit()
        return True

    @staticmethod
    def save_file_content(original_filename: str, content: bytes) -> tuple[str, str]:
        if not original_filename or not original_filename.strip():
            raise ValueError("Filename is required")

        os.makedirs(settings.STORAGE_BASE_PATH, exist_ok=True)

        trimmed_filename = original_filename.strip()
        file_ext = Path(trimmed_filename).suffix
        uuid_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.STORAGE_BASE_PATH, uuid_filename)

        with open(file_path, "wb") as f:
            f.write(content)

        return uuid_filename, f"/files/{uuid_filename}"

    @staticmethod
    def create_file_with_path(
        db: Session,
        original_filename: str,
        uuid_filename: str,
        storage_path: str,
        folderId: Optional[str] = None,
        mimeType: Optional[str] = None,
        size: Optional[int] = None,
    ) -> File:
        trimmed_filename = original_filename.strip()
        actual_folder_id = None if (folderId == "root" or not folderId) else folderId

        file = File(
            filename=uuid_filename,
            originalFilename=trimmed_filename,
            folderId=actual_folder_id,
            mimeType=mimeType,
            size=size,
            storagePath=f"{settings.API_BASE_URL}/files/{uuid_filename}"
        )
        db.add(file)
        db.commit()
        db.refresh(file)
        return file
