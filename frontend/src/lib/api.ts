import type { ChatMode, UploadMeta } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function uploadPdf(file: File): Promise<UploadMeta> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Upload failed");
  }
  return response.json();
}

interface ChatPayload {
  question: string;
  mode: ChatMode;
}

export interface ChatResponse {
  answer: string;
  chunks: string[];
}

export async function chatWithPaper(sessionId: string, payload: ChatPayload): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat/${sessionId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Chat request failed");
  }

  return response.json();
}
