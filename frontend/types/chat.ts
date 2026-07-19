export type Chat = {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
};

export type Message = {
  id: string;
  chat_id: string;
  role: "user" | "assistant" | string;
  content: string;
  created_at: string;
};

export type ChatListResponse = { chats: Chat[] };
export type ChatDetailResponse = Chat & { messages: Message[] };
export type ChatCreateResponse = { id: string; title: string };
export type ChatMessageResponse = {
  query: string;
  answer: string;
  sources?: unknown[];
};
