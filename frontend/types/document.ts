export type DocumentItem = {
  id: string;
  original_filename: string;
  file_path: string;
  file_type: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type DocumentListResponse = { documents: DocumentItem[] };
export type DocumentUploadResponse = {
  filename: string;
  document_id: string;
  message: string;
};
