export type ChatMode = "qa" | "explain-term" | "simplify";

export interface UploadMeta {
  session_id: string;
  filename?: string;
  chunk_count: number;
  character_count: number;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  mode?: ChatMode;
  sources?: string[];
}
