"use client";

import { Folder, Trash2 } from "lucide-react";
import { Folder as FolderType } from "@/lib/api-client";

interface FolderListProps {
  folders: FolderType[];
  onFolderClick: (id: string) => void;
  onDelete: (id: string) => void;
}

export function FolderList({
  folders,
  onFolderClick,
  onDelete,
}: FolderListProps) {
  return (
    <div className="space-y-2">
      {folders.length === 0 ? (
        <p className="text-sm text-gray-500 py-4">No folders</p>
      ) : (
        folders.map((folder) => (
          <div
            key={folder.id}
            className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition"
          >
            <button
              onClick={() => onFolderClick(folder.id)}
              className="flex items-center gap-2 flex-1 text-left hover:text-blue-600"
            >
              <Folder className="w-5 h-5 text-yellow-500 flex-shrink-0" />
              <span className="font-medium text-gray-900">{folder.name}</span>
            </button>
            <button
              onClick={() => onDelete(folder.id)}
              className="p-1 text-red-500 hover:bg-red-50 rounded transition"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))
      )}
    </div>
  );
}
