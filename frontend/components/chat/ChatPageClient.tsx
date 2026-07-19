"use client";

import { useEffect, useRef, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import { api } from "@/lib/api";
import type { ChatDetailResponse, Message } from "@/types/chat";

function createTemporaryId() {
  return `temp-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export default function ChatPageClient({ chatId }: { chatId: string }) {
  const [chat, setChat] = useState<ChatDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  async function loadChat() {
    try {
      setLoading(true);
      setError("");
      setChat(await api.getChat(chatId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load chat.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadChat();
  }, [chatId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat?.messages, sending]);

  async function sendMessage(content: string) {
     // Check before adding the temporary message.
  // The backend changes the title only after the first message.
    const isFirstMessage = chat?.messages.length === 0;
    const optimisticUser: Message = {
      id: createTemporaryId(),
      chat_id: chatId,
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };

    setChat((current) =>
      current ? { ...current, messages: [...current.messages, optimisticUser] } : current,
    );
    setSending(true);
    setError("");

    try {
      const result = await api.sendMessage(chatId, content);
      const assistantMessage: Message = {
        id: createTemporaryId(),
        chat_id: chatId,
        role: "assistant",
        content: result.answer,
        created_at: new Date().toISOString(),
      };
       // Show the assistant response immediately.
      setChat((current) =>
        current
          ? { ...current, messages: [...current.messages, assistantMessage] }
          : current,
      );
        // After the first message, fetch the chat again.
    // This gets the updated title from the backend without reloading the page.
      if (isFirstMessage) {
      const updatedChat = await api.getChat(chatId);
      setChat(updatedChat);

        // Notify AppShell that the sidebar chat list must refresh.
       window.dispatchEvent(new Event("chats-updated"));
}
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message.");
    } finally {
      setSending(false);
    }
  }

  return (
    <AppShell title={chat?.title || "Chat"} activeChatId={chatId}>
      <div className="flex h-[calc(100vh-4rem)] flex-col">
        <section className="flex-1 overflow-y-auto px-4 py-6 md:px-8">
          <div className="mx-auto max-w-4xl space-y-5">
            {loading && <p className="text-center text-sm text-slate-500">Loading chat...</p>}
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}
            {!loading && chat?.messages.length === 0 && (
              <div className="py-24 text-center">
                <h2 className="text-2xl font-semibold text-slate-900">Start a conversation</h2>
                <p className="mt-2 text-slate-500">
                  Ask a question based on the documents in your knowledge base.
                </p>
              </div>
            )}
            {chat?.messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {sending && (
              <div className="flex justify-start">
                <div className="rounded-2xl rounded-bl-md border border-slate-200 bg-white px-4 py-3 text-sm text-slate-500">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        </section>
        <ChatInput disabled={sending || loading} onSend={sendMessage} />
      </div>
    </AppShell>
  );
}
