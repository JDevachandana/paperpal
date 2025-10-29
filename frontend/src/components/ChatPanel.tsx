import { useState } from "react";
import type { ChatMode, Message } from "../types";
import { MessageBubble } from "./MessageBubble";

interface Props {
  sessionId?: string;
  messages: Message[];
  onSend: (payload: { question: string; mode: ChatMode }) => void;
  sending: boolean;
}

export function ChatPanel({ sessionId, messages, onSend, sending }: Props) {
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState<ChatMode>("qa");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!question.trim()) return;
    onSend({ question: question.trim(), mode });
    setQuestion("");
  };

  const disabled = !sessionId || sending;

  return (
    <div className="panel chat-panel">
      <h2>Ask anything</h2>
      {!sessionId && <p>Upload a PDF to unlock the chat workspace.</p>}
      <div className="messages">
        {messages.length === 0 && (
          <p style={{ color: "#94a3b8" }}>
            Try “What does the method section assume?” or “Simplify section 3 for a newcomer.”
          </p>
        )}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>
      <form className="chat-input" onSubmit={handleSubmit}>
        <textarea
          value={question}
          placeholder={sessionId ? "Type your question…" : "Upload a PDF to start chatting…"}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={!sessionId || sending}
        />
        <div className="chat-controls">
          <select value={mode} onChange={(event) => setMode(event.target.value as ChatMode)} disabled={!sessionId}>
            <option value="qa">Answer a question</option>
            <option value="explain-term">Explain a technical term</option>
            <option value="simplify">Simplify a passage</option>
          </select>
          <button type="submit" disabled={disabled}>
            {sending ? "Thinking…" : "Send"}
          </button>
        </div>
      </form>
    </div>
  );
}
