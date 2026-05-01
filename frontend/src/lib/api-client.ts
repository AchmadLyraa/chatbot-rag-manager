import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Types
export interface Folder {
  id: string;
  name: string;
  parentId: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface File {
  id: string;
  filename: string;
  originalFilename: string;
  storagePath: string;
  mimeType: string | null;
  size: number | null;
  folderId: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Folder API
export async function getFolders(parentId: string | null = null) {
  try {
    const params = parentId ? { parentId: parentId } : {};
    const response = await api.get<Folder[]>("/folders", { params });
    return { success: true, data: response.data };
  } catch (error) {
    console.error("[v0] Error fetching folders:", error);
    return { success: false, error: "Failed to fetch folders" };
  }
}

export async function createFolder(
  name: string,
  parentId: string | null = null,
) {
  try {
    const response = await api.post<Folder>("/folders", {
      name,
      parentId: parentId,
    });
    return { success: true, data: response.data };
  } catch (error) {
    console.error("[v0] Error creating folder:", error);
    return { success: false, error: "Failed to create folder" };
  }
}

export async function deleteFolder(id: string) {
  try {
    await api.delete(`/folders/${id}`);
    return { success: true };
  } catch (error) {
    console.error("[v0] Error deleting folder:", error);
    return { success: false, error: "Failed to delete folder" };
  }
}

// File API
export async function getFiles(folderId: string | null = null) {
  try {
    const params = folderId ? { folderId: folderId } : {};
    const response = await api.get<File[]>("/files", { params });
    return { success: true, data: response.data };
  } catch (error) {
    console.error("[v0] Error fetching files:", error);
    return { success: false, error: "Failed to fetch files" };
  }
}

export async function uploadFile(
  file: globalThis.File,
  folderId: string | null = null,
) {
  try {
    const formData = new FormData();

    formData.append("file", file);
    formData.append("filename", file.name);

    if (folderId) {
      formData.append("folderId", folderId);
    }

    const response = await api.post<File>("/files/upload", formData, {
      headers: {
        "Content-Type": undefined,
      },
    });
    return { success: true, data: response.data };
  } catch (error: any) {
    console.error("UPLOAD ERROR:", error.response?.data);
    return { success: false, error: "Failed to upload file" };
  }
}

export async function createFile(
  filename: string,
  folderId: string | null = null,
  size: number = 0,
) {
  try {
    const payload = {
      filename: filename.trim(),
      folderId: folderId || null,
      mimeType: getMimeType(filename),
      size: size,
    };
    const response = await api.post<File>("/files", payload);
    return { success: true, data: response.data };
  } catch (error) {
    console.error("[v0] Error creating file:", error);
    return { success: false, error: "Failed to create file" };
  }
}

function getMimeType(filename: string): string {
  const ext = filename.split(".").pop()?.toLowerCase() || "";
  const mimeMap: Record<string, string> = {
    pdf: "application/pdf",
    doc: "application/msword",
    docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    txt: "text/plain",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    webp: "image/webp",
  };
  return mimeMap[ext] || "application/octet-stream";
}

export async function deleteFile(id: string) {
  try {
    await api.delete(`/files/${id}`);
    return { success: true };
  } catch (error) {
    console.error("[v0] Error deleting file:", error);
    return { success: false, error: "Failed to delete file" };
  }
}
