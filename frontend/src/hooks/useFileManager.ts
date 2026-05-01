"use client";

import { useState, useCallback, useEffect } from "react";
import {
  getFolders,
  getFiles,
  createFolder as apiCreateFolder,
  createFile as apiCreateFile,
  uploadFile as apiUploadFile,
  deleteFolder as apiDeleteFolder,
  deleteFile as apiDeleteFile,
  Folder,
  File,
} from "@/lib/api-client";

export function useFileManager() {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [files, setFiles] = useState<File[]>([]);
  const [currentFolderId, setCurrentFolderId] = useState<string | null>(null);
  const [breadcrumbs, setBreadcrumbs] = useState<
    (Folder | { id: null; name: string })[]
  >([{ id: null, name: "Home" }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Create folder
  const createFolder = useCallback(
    async (name: string, parentId: string | null = null) => {
      const result = await apiCreateFolder(name, parentId);
      if (result.success && result.data) {
        setFolders((prev) => [...prev, result.data as Folder]);
        setError(null);
        return result.data;
      } else {
        setError(result.error || "Failed to create folder");
        return null;
      }
    },
    [],
  );

  // Upload file with binary content
  const uploadFile = useCallback(
    async (file: globalThis.File, folderId: string | null = null) => {
      setError(null);
      try {
        const result = await apiUploadFile(file, folderId);
        if (result.success && result.data) {
          setFiles((prev) => [...prev, result.data as File]);
          return result.data;
        } else {
          setError(result.error || "Failed to upload file");
          return null;
        }
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : "Unknown error";
        setError(errorMsg);
        return null;
      }
    },
    [],
  );

  // Create file metadata only (without binary)
  const createFile = useCallback(
    async (
      filename: string,
      folderId: string | null = null,
      size: number = 0,
    ) => {
      const result = await apiCreateFile(filename, folderId, size);
      if (result.success && result.data) {
        setFiles((prev) => [...prev, result.data as File]);
        setError(null);
        return result.data;
      } else {
        setError(result.error || "Failed to create file");
        return null;
      }
    },
    [],
  );

  // Delete folder
  const deleteFolder = useCallback(async (folderId: string) => {
    const result = await apiDeleteFolder(folderId);
    if (result.success) {
      setFolders((prev) => prev.filter((f) => f.id !== folderId));
      setError(null);
      return true;
    } else {
      setError(result.error || "Failed to delete folder");
      return false;
    }
  }, []);

  // Delete file
  const deleteFile = useCallback(async (fileId: string) => {
    const result = await apiDeleteFile(fileId);
    if (result.success) {
      setFiles((prev) => prev.filter((f) => f.id !== fileId));
      setError(null);
      return true;
    } else {
      setError(result.error || "Failed to delete file");
      return false;
    }
  }, []);

  const load = useCallback(async (folderId: string | null) => {
    setLoading(true);
    setError(null);

    const [fRes, fiRes] = await Promise.all([
      getFolders(folderId),
      getFiles(folderId),
    ]);

    if (fRes.success) setFolders(fRes.data || []);
    else setError(fRes.error || "Failed folders");

    if (fiRes.success) setFiles(fiRes.data || []);
    else setError(fiRes.error || "Failed files");

    setLoading(false);
  }, []);

  // Navigate to folder
  const navigateToFolder = useCallback(
    async (folderId: string | null) => {
      setCurrentFolderId(folderId);

      await load(folderId);

      // Build breadcrumbs by traversing parent chain
      if (!folderId) {
        setBreadcrumbs([{ id: null, name: "Home" }]);
      } else {
        const path: Folder[] = [];
        let currentId: string | null = folderId;
        const visited = new Set<string>();

        while (currentId && !visited.has(currentId)) {
          visited.add(currentId);
          try {
            const folderResult = await fetch(
              `http://localhost:8000/api/v1/folders/${currentId}`,
            ).then((res) => res.json());

            if (folderResult && folderResult.id) {
              const folder: Folder = folderResult;
              path.unshift(folder);
              currentId = folder.parentId;
            } else {
              break;
            }
          } catch (err) {
            console.error("Error getting folder:", err);
            break;
          }
        }

        setBreadcrumbs([{ id: null, name: "Home" }, ...path]);
      }
    },
    [load],
  );

  // Initialize
  useEffect(() => {
    navigateToFolder(null);
  }, [navigateToFolder]);

  return {
    folders,
    files,
    currentFolderId,
    breadcrumbs,
    loading,
    error,
    createFolder,
    createFile,
    uploadFile,
    deleteFolder,
    deleteFile,
    navigateToFolder,
  };
}
