"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { BookOpen, MessageSquarePlus } from "lucide-react";
import AppShell from "@/components/layout/AppShell";
import { api } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [creating, setCreating] = useState(false);

  async function createChat() {
    try {
      setCreating(true);
      const chat = await api.createChat();
      router.push(`/chats/${chat.id}`);
    } finally {
      setCreating(false);
    }
  }

  return (
    <AppShell title="Research Assistant">
      <div className="grid min-h-[calc(100vh-4rem)] place-items-center p-6">
        <div className="max-w-xl text-center">
          <span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-blue-600 text-white shadow-soft">
            <BookOpen size={30} />
          </span>
          <h2 className="mt-6 text-3xl font-bold text-slate-900">
            Ask questions from your knowledge base
          </h2>
          <p className="mt-3 text-slate-500">
            Upload your documents, create a chat, and get answers from your research material.
          </p>
          <button
            onClick={createChat}
            disabled={creating}
            className="mt-7 inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            <MessageSquarePlus size={19} />
            {creating ? "Creating..." : "Start New Chat"}
          </button>
        </div>
      </div>
    </AppShell>
  );
}
