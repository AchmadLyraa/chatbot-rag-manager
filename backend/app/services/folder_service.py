from sqlalchemy.orm import Session
from app.models.folder import Folder
from typing import List, Optional
import os
from app.core.config import settings


class FolderService:
    @staticmethod
    def get_folders(db: Session, parentId: Optional[str] = None) -> List[Folder]:
        query = db.query(Folder)
        if parentId:
            query = query.filter(Folder.parentId == parentId)
        else:
            query = query.filter(Folder.parentId == None)
        return query.order_by(Folder.name).all()

    @staticmethod
    def get_folder_by_id(db: Session, folder_id: str) -> Optional[Folder]:
        return db.query(Folder).filter(Folder.id == folder_id).first()

    @staticmethod
    def create_folder(db: Session, name: str, parentId: Optional[str] = None) -> Folder:
        if not name or not name.strip():
            raise ValueError("Folder name is required")

        if parentId:
            parent = db.query(Folder).filter(Folder.id == parentId).first()
            if not parent:
                raise ValueError("Parent folder not found")

        folder = Folder(
            name=name.strip(),
            parentId=parentId if parentId else None
        )
        db.add(folder)
        db.commit()
        db.refresh(folder)
        return folder

    @staticmethod
    def delete_folder(db: Session, folder_id: str) -> bool:
        if not folder_id:
            raise ValueError("Folder ID is required")

        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            return False

        def get_all_descendant_ids(parent_id: str) -> List[str]:
            children = db.query(Folder.id).filter(Folder.parentId == parent_id).all()
            ids = [child[0] for child in children]
            for child_id in ids:
                ids.extend(get_all_descendant_ids(child_id))
            return ids

        descendant_ids = get_all_descendant_ids(folder_id)
        all_folder_ids = [folder_id] + descendant_ids

        # Hapus file fisik + metadata di semua folder
        from app.models.file import File
        for fid in all_folder_ids:
            files = db.query(File).filter(File.folderId == fid).all()
            for f in files:
                try:
                    file_path = os.path.join(settings.STORAGE_BASE_PATH, f.filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not delete physical file: {e}")
                db.delete(f)

        # Hapus subfolder dari yang paling dalam dulu, baru folder utama
        for fid in reversed(descendant_ids):
            subfolder = db.query(Folder).filter(Folder.id == fid).first()
            if subfolder:
                db.delete(subfolder)

        db.delete(folder)
        db.commit()
        return True

    @staticmethod
    def get_folder_by_id_with_children(db: Session, folder_id: str) -> Optional[Folder]:
        return db.query(Folder).filter(Folder.id == folder_id).first()
