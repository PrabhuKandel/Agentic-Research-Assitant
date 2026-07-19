"use client";

import { UploadCloud } from "lucide-react";
import { useRef, useState } from "react";

interface DocumentUploadProps {
  uploading: boolean;
  onUpload: (file: File) => Promise<void>;
}

export default function DocumentUpload({ uploading, onUpload }: DocumentUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function selectFile(file?: File) {
    if (file) onUpload(file);
  }

  return (
    <div
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(event) => {
        event.preventDefault();
        setDragging(false);
        selectFile(event.dataTransfer.files[0]);
      }}
      className={`rounded-2xl border-2 border-dashed p-8 text-center transition ${
        dragging ? "border-blue-500 bg-blue-50" : "border-slate-300 bg-white"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf,.txt"
        onChange={(event) => selectFile(event.target.files?.[0])}
      />
      <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-blue-50 text-blue-600">
        <UploadCloud size={28} />
      </span>
      <h3 className="mt-4 text-lg font-semibold text-slate-900">
        Upload a document
      </h3>
      <p className="mt-2 text-sm text-slate-500">
        Drag and drop a PDF or TXT file here, or choose a file from your computer.
      </p>
      <button
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
        className="mt-5 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {uploading ? "Uploading and processing..." : "Choose File"}
      </button>
    </div>
  );
}
