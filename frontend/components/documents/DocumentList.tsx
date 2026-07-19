"use client";

import { FileText, Trash2 } from "lucide-react";
import { formatDate, getFileExtension } from "@/lib/utils";
import type { DocumentItem } from "@/types/document";

interface DocumentListProps {
  documents: DocumentItem[];
  deletingId: string | null;
  onDelete: (documentId: string) => Promise<void>;
}

export default function DocumentList({
  documents,
  deletingId,
  onDelete,
}: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center text-sm text-slate-500">
        No documents uploaded yet.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-5 py-4 font-semibold">Document</th>
              <th className="px-5 py-4 font-semibold">Type</th>
              <th className="px-5 py-4 font-semibold">Uploaded</th>
              <th className="px-5 py-4 font-semibold">Status</th>
              <th className="px-5 py-4 text-right font-semibold">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {documents.map((document) => (
              <tr key={document.id} className="hover:bg-slate-50">
                <td className="px-5 py-4">
                  <div className="flex min-w-[240px] items-center gap-3">
                    <span className="grid h-10 w-10 place-items-center rounded-xl bg-blue-50 text-blue-600">
                      <FileText size={19} />
                    </span>
                    <span className="max-w-sm truncate font-medium text-slate-800">
                      {document.original_filename}
                    </span>
                  </div>
                </td>
                <td className="px-5 py-4 text-slate-600">
                  {getFileExtension(document.original_filename)}
                </td>
                <td className="px-5 py-4 text-slate-600">
                  {formatDate(document.created_at)}
                </td>
                <td className="px-5 py-4">
                  <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium capitalize text-emerald-700">
                    {document.status}
                  </span>
                </td>
                <td className="px-5 py-4 text-right">
                  <button
                    onClick={() => onDelete(document.id)}
                    disabled={deletingId === document.id}
                    className="rounded-lg p-2 text-slate-400 hover:bg-red-50 hover:text-red-600 disabled:opacity-40"
                    title="Delete document"
                  >
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
