"use client";

import { Menu } from "lucide-react";
import { useEffect, useState, useCallback } from "react";
import Sidebar from "./Sidebar";
import { api } from "@/lib/api";
import type { Chat } from "@/types/chat";

interface AppShellProps {
  children: React.ReactNode;
  title: string;
  activeChatId?: string;
}

export default function AppShell({ children, title, activeChatId }: AppShellProps) {
  const [chats, setChats] = useState<Chat[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Keep the same function reference between renders.
const loadChats = useCallback(async () => {
  try {
    const data = await api.listChats();
    setChats(data.chats);
  } catch {
    setChats([]);
  }
}, []);

  useEffect(() => {
    loadChats();
  }, [loadChats]);

  // Refresh the sidebar when ChatPageClient says the title changed.
  useEffect(() => {
    function handleChatsUpdated() {
      loadChats();
    }

    window.addEventListener("chats-updated", handleChatsUpdated);

    return () => {
      window.removeEventListener("chats-updated", handleChatsUpdated);
    };
  }, [loadChats]);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onChatsChanged={loadChats}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center gap-3 border-b border-slate-200 bg-white px-4 lg:px-8">
          <button
            className="rounded-lg p-2 hover:bg-slate-100 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={21} />
          </button>
          <h1 className="truncate text-lg font-semibold text-slate-900">{title}</h1>
        </header>
        <main className="min-h-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
