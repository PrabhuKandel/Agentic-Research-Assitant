"use client";

import { useEffect, useState } from "react";
import {toast} from "sonner"
import AppShell from "@/components/layout/AppShell";
import DocumentList from "./DocumentList";
import DocumentUpload from "./DocumentUpload";
import { api } from "@/lib/api";
import type { DocumentItem } from "@/types/document";

export default function DocumentsPageClient() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);


  async function loadDocuments() {
    try {
      setLoading(true);
      const data = await api.listDocuments();
      setDocuments(data.documents);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Could not load documents.";
      //show the loading error as a toast notification
      toast.error(message);

    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  async function upload(file: File) {
    try {
      setUploading(true);
      toast.dismiss(); // Dismiss any existing toasts
      const result = await api.uploadDocument(file);
      toast.success(result.message);
      await loadDocuments();
    } catch (err) {
         const message =
        err instanceof Error
          ? err.message
          : "Upload failed.";

      toast.error(message);
    } finally {
      setUploading(false);
    }
  }

  async function remove(documentId: string) {
    const confirmed = window.confirm("Delete this document and its stored chunks?");
    if (!confirmed) return;

    try {
      setDeletingId(documentId);
 
      const result = await api.deleteDocument(documentId);

      // Show delete success notification.
      toast.success(result.message);
    
      setDocuments((current) => current.filter((item) => item.id !== documentId));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Delete failed.";
      toast.error(message);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <AppShell title="Knowledge Base">
      <div className="mx-auto max-w-6xl space-y-8 p-4 md:p-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Knowledge Base</h2>
          <p className="mt-2 text-slate-500">
            Upload and manage the documents used by your research assistant.
          </p>
        </div>

        <DocumentUpload uploading={uploading} onUpload={upload} />

        <section>
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-slate-900">Document Library</h3>
            <span className="text-sm text-slate-500">{documents.length} document(s)</span>
          </div>
          {loading ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center text-sm text-slate-500">
              Loading documents...
            </div>
          ) : (
            <DocumentList
              documents={documents}
              deletingId={deletingId}
              onDelete={remove}
            />
          )}
        </section>
      </div>
    </AppShell>
  );
}
