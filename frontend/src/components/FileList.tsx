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
  onIndex: (id: string) => Promise<void>;
}

export function FileList({ files, onDelete, onIndex }: FileListProps) {
  const [previewFile, setPreviewFile] = useState<FileType | null>(null);
  const [indexingId, setIndexingId] = useState<string | null>(null);

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

                    {file.indexed && (
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                        Indexed
                      </span>
                    )}
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

                    {!file.indexed && (
                      <button
                        disabled={indexingId === file.id}
                        onClick={async () => {
                          try {
                            setIndexingId(file.id);
                            await onIndex(file.id);
                          } finally {
                            setIndexingId(null);
                          }
                        }}
                        className={`px-2 py-1 rounded text-xs font-medium transition ${
                          indexingId === file.id
                            ? "bg-gray-200 text-gray-500 cursor-not-allowed"
                            : "bg-green-100 text-green-700 hover:bg-green-200"
                        }`}
                        title="Index"
                      >
                        {indexingId === file.id ? "Indexing..." : "Index"}
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
          className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
          onClick={() => setPreviewFile(null)}
        >
          <div
            className="bg-white rounded-xl w-[95vw] h-[95vh] flex flex-col overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b">
              <h3 className="font-semibold truncate">
                {previewFile.originalFilename}
              </h3>

              <button
                onClick={() => setPreviewFile(null)}
                className="text-2xl text-gray-500 hover:text-black"
              >
                ×
              </button>
            </div>

            {/* Body */}
            <div className="flex-1 overflow-hidden">
              {/* IMAGE */}
              {previewFile.mimeType?.startsWith("image/") && (
                <div className="w-full h-full flex items-center justify-center bg-gray-100">
                  <img
                    src={previewFile.storagePath}
                    alt={previewFile.originalFilename}
                    className="max-w-full max-h-full object-contain"
                  />
                </div>
              )}

              {/* PDF */}
              {previewFile.mimeType === "application/pdf" && (
                <iframe
                  src={previewFile.storagePath}
                  className="w-full h-full"
                />
              )}

              {/* TEXT */}
              {previewFile.mimeType?.startsWith("text/") && (
                <div className="w-full h-full overflow-auto p-4 font-mono text-sm">
                  Loading text content...
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
