"use client";

import { Send } from "lucide-react";
import { useState } from "react";

interface ChatInputProps {
  disabled: boolean;
  onSend: (message: string) => Promise<void>;
}

export default function ChatInput({ disabled, onSend }: ChatInputProps) {
  const [message, setMessage] = useState("");

  async function submit() {
    const trimmed = message.trim();
    if (!trimmed || disabled) return;
    setMessage("");
    await onSend(trimmed);
  }

  return (
    <div className="border-t border-slate-200 bg-white p-4 md:p-6">
      <div className="mx-auto flex max-w-4xl items-end gap-3 rounded-2xl border border-slate-300 bg-white p-3 shadow-soft focus-within:border-blue-500">
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              submit();
            }
          }}
          rows={1}
          placeholder="Ask a question about your documents..."
          className="max-h-40 min-h-11 flex-1 resize-none border-0 bg-transparent px-2 py-2 text-sm outline-none"
          disabled={disabled}
        />
        <button
          onClick={submit}
          disabled={disabled || !message.trim()}
          className="grid h-11 w-11 place-items-center rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <Send size={18} />
        </button>
      </div>
      <p className="mx-auto mt-2 max-w-4xl text-center text-xs text-slate-400">
        Enter to send · Shift + Enter for a new line
      </p>
    </div>
  );
}
