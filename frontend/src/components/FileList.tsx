"use client";

import { useState } from "react";
import {
  FileText,
  Image,
  File,
  Trash2,
  Eye,
  FileJson,
  FileCode,
} from "lucide-react";
import { File as FileType } from "@/lib/api-client";
import { formatFileSize, formatDate } from "@/lib/utils";

interface FileListProps {
  files: FileType[];
  onDelete: (id: string) => void;
}

export function FileList({ files, onDelete }: FileListProps) {
  const [previewFile, setPreviewFile] = useState<FileType | null>(null);

  const getFileIcon = (filename: string, mimeType: string | null) => {
    const ext = filename.split(".").pop()?.toLowerCase() || "";

    if (mimeType?.startsWith("image/")) {
      return <Image className="w-5 h-5 text-green-500" />;
    }
    if (mimeType === "application/pdf") {
      return <FileText className="w-5 h-5 text-red-500" />;
    }
    if (
      mimeType ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
      ext === "doc" ||
      ext === "docx"
    ) {
      return <FileText className="w-5 h-5 text-blue-500" />;
    }
    if (mimeType?.startsWith("text/")) {
      return <FileCode className="w-5 h-5 text-gray-600" />;
    }
    if (ext === "json") {
      return <FileJson className="w-5 h-5 text-yellow-600" />;
    }

    return <File className="w-5 h-5 text-gray-500" />;
  };

  const canPreview = (mimeType: string | null) => {
    return (
      mimeType?.startsWith("image/") ||
      mimeType === "application/pdf" ||
      mimeType?.startsWith("text/")
    );
  };

  if (files.length === 0) {
    return <p className="text-sm text-gray-500 py-4">No files</p>;
  }

  return (
    <>
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 border-b border-gray-200">
            <tr>
              <th className="text-left p-3 font-semibold text-gray-900">
                Name
              </th>
              <th className="text-left p-3 font-semibold text-gray-900">
                Size
              </th>
              <th className="text-left p-3 font-semibold text-gray-900">
                Modified
              </th>
              <th className="text-center p-3 font-semibold text-gray-900">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr
                key={file.id}
                className="border-b border-gray-200 hover:bg-gray-50"
              >
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    {getFileIcon(file.originalFilename, file.mimeType)}
                    <span className="text-gray-900 font-medium">
                      {file.originalFilename}
                    </span>
                  </div>
                </td>
                <td className="p-3 text-gray-600">
                  {file.size ? formatFileSize(file.size) : "-"}
                </td>
                <td className="p-3 text-gray-600">
                  {formatDate(new Date(file.createdAt))}
                </td>
                <td className="p-3">
                  <div className="flex items-center justify-center gap-2">
                    {canPreview(file.mimeType) && (
                      <button
                        onClick={() => setPreviewFile(file)}
                        className="p-1 text-blue-500 hover:bg-blue-50 rounded transition"
                        title="Preview"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => onDelete(file.id)}
                      className="p-1 text-red-500 hover:bg-red-50 rounded transition"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Preview Modal */}
      {previewFile && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={() => setPreviewFile(null)}
        >
          <div
            className="bg-white rounded-lg p-6 max-w-2xl max-h-96 overflow-auto shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">
                {previewFile.originalFilename}
              </h3>
              <button
                onClick={() => setPreviewFile(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ×
              </button>
            </div>

            {/* Image Preview */}
            {previewFile.mimeType?.startsWith("image/") && (
              <img
                src={previewFile.storagePath}
                alt={previewFile.originalFilename}
                className="w-full h-auto rounded"
              />
            )}

            {/* PDF Preview */}
            {previewFile.mimeType === "application/pdf" && (
              <iframe
                src={previewFile.storagePath}
                className="w-full h-96 rounded"
              />
            )}

            {/* Text File Preview */}
            {previewFile.mimeType?.startsWith("text/") && (
              <div className="bg-gray-100 p-4 rounded font-mono text-sm whitespace-pre-wrap break-words">
                Loading text content...
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
