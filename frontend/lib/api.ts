import type {
  ChatCreateResponse,
  ChatDetailResponse,
  ChatListResponse,
  ChatMessageResponse,
} from "@/types/chat";
import type {
  DocumentListResponse,
  DocumentUploadResponse,
} from "@/types/document";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options?.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
      ...options?.headers,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let message = "Something went wrong.";
    try {
      const data = await response.json();
      message = data.detail ?? data.message ?? message;
    } catch {
      // Keep default message if response is not JSON.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export const api = {
  listChats: () => request<ChatListResponse>("/chats"),
  createChat: () =>
    request<ChatCreateResponse>("/chats", { method: "POST" }),
  getChat: (chatId: string) =>
    request<ChatDetailResponse>(`/chats/${chatId}`),
  deleteChat: (chatId: string) =>
    request<{ message: string }>(`/chats/${chatId}`, { method: "DELETE" }),
  sendMessage: (chatId: string, query: string) =>
    request<ChatMessageResponse>(`/chats/${chatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ query }),
    }),

  listDocuments: () => request<DocumentListResponse>("/documents"),
  uploadDocument: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<DocumentUploadResponse>("/documents/upload", {
      method: "POST",
      body: formData,
    });
  },
  deleteDocument: (documentId: string) =>
    request<{ document_id: string; message: string }>(
      `/documents/${documentId}`,
      { method: "DELETE" },
    ),
};
