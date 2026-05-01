"use client";

import { Home, ChevronRight } from "lucide-react";
import { Folder } from "@/lib/api-client";

interface BreadcrumbProps {
  items: (Folder | { id: null; name: string })[];
  onNavigate: (id: string | null) => void;
}

export function Breadcrumb({ items, onNavigate }: BreadcrumbProps) {
  return (
    <div className="flex items-center gap-1 text-sm">
      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-1">
          {index > 0 && <ChevronRight className="w-4 h-4 text-gray-400" />}
          <button
            onClick={() => onNavigate(item.id)}
            className="flex items-center gap-1 px-2 py-1 text-gray-700 hover:text-blue-600 hover:bg-gray-100 rounded transition"
          >
            {item.id === null && <Home className="w-4 h-4" />}
            {item.name}
          </button>
        </div>
      ))}
    </div>
  );
}
