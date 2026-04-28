"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input,
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    const assistantId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: assistantId, role: "assistant", content: "" },
    ]);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages: updatedMessages.map((m) => ({
              role: m.role,
              content: m.content,
            })),
          }),
        },
      );

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, content: m.content + chunk } : m,
          ),
        );
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col w-full max-w-2xl py-24 mx-auto">
      <div className="flex flex-col gap-4 mb-24">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`p-3 rounded-lg whitespace-pre-wrap ${
              m.role === "user"
                ? "bg-blue-100 dark:bg-blue-900 self-end max-w-lg"
                : "bg-zinc-100 dark:bg-zinc-800 self-start max-w-lg"
            }`}
          >
            <span className="text-xs font-bold block mb-1 opacity-60">
              {m.role === "user" ? "Kamu" : "AI"}
            </span>
            {m.content || (loading && m.role === "assistant" ? "..." : "")}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form
        onSubmit={sendMessage}
        className="fixed bottom-0 w-full max-w-2xl mb-8 flex gap-2"
      >
        <input
          className="flex-1 p-3 border border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 rounded-lg shadow-xl"
          value={input}
          placeholder="Tanya sesuatu..."
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-3 bg-blue-600 text-white rounded-lg disabled:opacity-50"
        >
          Kirim
        </button>
      </form>
    </div>
  );
}
