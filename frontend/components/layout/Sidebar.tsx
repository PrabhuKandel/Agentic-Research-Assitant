"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { BookOpen, MessageSquarePlus, Trash2, X } from "lucide-react";
import { api } from "@/lib/api";
import type { Chat } from "@/types/chat";
import {toast} from "sonner"

interface SidebarProps {
  chats: Chat[];
  activeChatId?: string;
  open: boolean;
  onClose: () => void;
  onChatsChanged: () => void;
}

export default function Sidebar({
  chats,
  activeChatId,
  open,
  onClose,
  onChatsChanged,
}: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

  async function handleNewChat() {
    const chat = await api.createChat();
    onChatsChanged();
    router.push(`/chats/${chat.id}`);
    onClose();
  }

  async function handleDeleteChat(chatId: string) {
    const confirmed = window.confirm("Delete this chat?");
    if (!confirmed) return;
    try{
    await api.deleteChat(chatId);
        onChatsChanged();
            // Show success notification.
    toast.success("Chat deleted successfully.");

    // Redirect only when the currently open chat was deleted.
    if (activeChatId === chatId) {
      router.push("/");
    }
  } catch (err) {
    const message =
      err instanceof Error
        ? err.message
        : "Failed to delete chat.";

    toast.error(message);
  }
}
  
  return (
    <>
      {open && (
        <button
          aria-label="Close sidebar overlay"
          className="fixed inset-0 z-30 bg-slate-950/30 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-slate-200 bg-white p-4 transition-transform lg:static lg:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="mb-6 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 font-semibold text-slate-900">
            <span className="grid h-10 w-10 place-items-center rounded-xl bg-blue-600 text-white">
              <BookOpen size={20} />
            </span>
            <span>Research Assistant</span>
          </Link>
          <button className="rounded-lg p-2 hover:bg-slate-100 lg:hidden" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <button
          onClick={handleNewChat}
          className="mb-4 flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 font-medium text-white hover:bg-blue-700"
        >
          <MessageSquarePlus size={18} /> New Chat
        </button>

        <Link
          href="/documents"
          onClick={onClose}
          className={`mb-5 flex items-center gap-2 rounded-xl px-3 py-3 font-medium ${
            pathname === "/documents"
              ? "bg-blue-50 text-blue-700"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          <BookOpen size={18} /> Knowledge Base
        </Link>

        <p className="mb-2 px-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Recent chats
        </p>

        <div className="flex-1 space-y-1 overflow-y-auto">
          {chats.length === 0 ? (
            <p className="px-2 py-3 text-sm text-slate-400">No chats yet.</p>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                className={`group flex items-center rounded-xl ${
                  activeChatId === chat.id ? "bg-blue-50" : "hover:bg-slate-100"
                }`}
              >
                <Link
                  href={`/chats/${chat.id}`}
                  onClick={onClose}
                  className="min-w-0 flex-1 truncate px-3 py-2.5 text-sm text-slate-700"
                >
                  {chat.title || "New chat"}
                </Link>
                <button
                  title="Delete chat"
                  onClick={() => handleDeleteChat(chat.id)}
                  className="mr-2 rounded-md p-1.5 text-slate-400 opacity-0 hover:bg-red-50 hover:text-red-600 group-hover:opacity-100"
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>
    </>
  );
}
