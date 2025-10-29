import { useRef } from "react";
import type { UploadMeta } from "../types";

interface Props {
  uploading: boolean;
  meta?: UploadMeta;
  onUpload: (file: File) => void;
}

export function UploadPanel({ uploading, meta, onUpload }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.name.toLowerCase().endswith(".pdf")) {
      alert("Please choose a PDF file.");
      return;
    }
    onUpload(file);
    event.target.value = "";
  };

  return (
    <div className="panel">
      <h2>Upload your paper</h2>
      <p>Drop in a PDF and we&apos;ll create an explainable knowledge base for the conversation.</p>
      <div
        className="file-drop"
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(event) => event.key === "Enter" && inputRef.current?.click()}
      >
        {uploading ? (
          <strong>Processing PDF…</strong>
        ) : (
          <>
            <strong>Click to select a PDF</strong>
            <p style={{ marginTop: "0.5rem" }}>We keep everything local — no cloud storage required.</p>
          </>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      {meta && (
        <div className="upload-meta">
          <p style={{ margin: 0, fontWeight: 600 }}>{meta.filename}</p>
          <p style={{ margin: "0.4rem 0 0" }}>
            Session: <code>{meta.session_id}</code>
          </p>
          <p style={{ margin: "0.2rem 0 0" }}>
            {meta.chunk_count} knowledge chunks • {meta.character_count.toLocaleString()} characters
          </p>
          <span className="status-pill">Ready</span>
        </div>
      )}
    </div>
  );
}
