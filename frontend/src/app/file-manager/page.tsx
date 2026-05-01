"use client";

import { useFileManager } from "@/hooks/useFileManager";
import { FolderList } from "@/components/FolderList";
import { FileList } from "@/components/FileList";
import { FolderActions } from "@/components/FolderActions";
import { Breadcrumb } from "@/components/Breadcrumb";
import Link from "next/link";

export default function FileManagerPage() {
  const {
    folders,
    files,
    currentFolderId,
    breadcrumbs,
    loading,
    error,
    createFolder,
    uploadFile,
    deleteFolder,
    deleteFile,
    navigateToFolder,
  } = useFileManager();

  return (
    <main className="min-h-screen bg-gray-100">
      <Link
        href="/"
        className="fixed top-4 right-4 px-4 py-2 bg-black text-white rounded"
      >
        Chatbot
      </Link>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            File Manager
          </h1>
          <Breadcrumb items={breadcrumbs} onNavigate={navigateToFolder} />
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Actions */}
        <div className="mb-6">
          <FolderActions
            onCreateFolder={(name) => createFolder(name, currentFolderId)}
            onUploadFile={(file) => uploadFile(file, currentFolderId)}
          />
        </div>

        {/* Loading */}
        {loading ? (
          <div className="text-center py-12">
            <p>Loading...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Folder */}
            <div>
              <h2 className="text-lg font-semibold mb-3">Folders</h2>
              <FolderList
                folders={folders}
                onFolderClick={navigateToFolder}
                onDelete={deleteFolder}
              />
            </div>

            {/* Files */}
            <div className="lg:col-span-2">
              <h2 className="text-lg font-semibold mb-3">Files</h2>
              <FileList files={files} onDelete={deleteFile} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
