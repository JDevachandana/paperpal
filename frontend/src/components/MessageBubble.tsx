import type { Message } from "../types";

interface Props {
  message: Message;
}

export function MessageBubble({ message }: Props) {
  return (
    <div className={`message ${message.role}`}>
      <div>{message.content}</div>
      {message.role === "assistant" && message.sources && message.sources.length > 0 && (
        <div className="sources">
          <strong>Context</strong>
          <ul style={{ margin: "0.4rem 0 0", paddingLeft: "1.1rem" }}>
            {message.sources.map((chunk) => (
              <li key={chunk}>{chunk}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
