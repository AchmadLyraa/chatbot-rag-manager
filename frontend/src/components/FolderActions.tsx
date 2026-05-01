"use client";

import { useState, useRef } from "react";
import { FolderPlus, Upload } from "lucide-react";

interface FolderActionsProps {
  onCreateFolder: (name: string) => Promise<void>;
  onUploadFile: (file: File) => Promise<void>;
}

export function FolderActions({
  onCreateFolder,
  onUploadFile,
}: FolderActionsProps) {
  const [folderName, setFolderName] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [showDialog, setShowDialog] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleCreateFolder = async () => {
    if (!folderName.trim()) return;

    setIsCreating(true);
    try {
      await onCreateFolder(folderName.trim());
      setFolderName("");
      setShowDialog(false);
    } catch (error) {
      console.error("[v0] Error creating folder:", error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files;
    if (!files) return;

    setIsUploading(true);
    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        await onUploadFile(file);
      }
    } catch (error) {
      console.error("[v0] Error uploading files:", error);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  return (
    <div className="flex gap-2">
      {/* Create Folder Button */}
      <button
        onClick={() => setShowDialog(true)}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        <FolderPlus className="w-4 h-4" />
        New Folder
      </button>

      {/* Upload File Button */}
      <label className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition cursor-pointer">
        <Upload className="w-4 h-4" />
        Upload File
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileUpload}
          disabled={isUploading}
          className="hidden"
        />
      </label>

      {/* Create Folder Dialog */}
      {showDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 shadow-lg">
            <h2 className="text-lg font-semibold mb-4">Create New Folder</h2>
            <input
              type="text"
              placeholder="Folder name"
              value={folderName}
              onChange={(e) => setFolderName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !isCreating) {
                  handleCreateFolder();
                }
              }}
              autoFocus
              className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowDialog(false);
                  setFolderName("");
                }}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateFolder}
                disabled={!folderName.trim() || isCreating}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {isCreating ? "Creating..." : "Create"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
