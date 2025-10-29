import { useState } from "react";
import { UploadPanel } from "./components/UploadPanel";
import { ChatPanel } from "./components/ChatPanel";
import { chatWithPaper, uploadPdf } from "./lib/api";
import type { ChatMode, Message, UploadMeta } from "./types";

const makeId = () => crypto.randomUUID?.() ?? Math.random().toString(36).slice(2);

function App() {
  const [uploadMeta, setUploadMeta] = useState<UploadMeta>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [uploading, setUploading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const meta = await uploadPdf(file);
      setUploadMeta(meta);
      setMessages([]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Upload failed";
      setError(message);
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async ({ question, mode }: { question: string; mode: ChatMode }) => {
    if (!uploadMeta) return;
    setError(null);
    const userMessage: Message = {
      id: makeId(),
      role: "user",
      content: question,
      mode,
    };
    setMessages((prev) => [...prev, userMessage]);
    setSending(true);
    try {
      const response = await chatWithPaper(uploadMeta.session_id, { question, mode });
      const assistantMessage: Message = {
        id: makeId(),
        role: "assistant",
        content: response.answer,
        mode,
        sources: response.chunks,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong";
      setError(message);
      setMessages((prev) => [
        ...prev,
        {
          id: makeId(),
          role: "assistant",
          content: `⚠️ ${message}`,
          mode,
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Paperpal</h1>
        <p>Explain technical terms, simplify dense sections, and ask grounded questions about your papers.</p>
        {error && (
          <p style={{ color: "#b91c1c", marginTop: "0.5rem" }}>
            {error}
          </p>
        )}
      </header>
      <main className="app-content">
        <UploadPanel uploading={uploading} meta={uploadMeta} onUpload={handleUpload} />
        <ChatPanel
          sessionId={uploadMeta?.session_id}
          messages={messages}
          onSend={handleSend}
          sending={sending}
        />
      </main>
    </div>
  );
}

export default App;
