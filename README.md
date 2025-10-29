# Paperpal — chat with your papers

Paperpal is a local-first FastAPI + React assistant that ingests PDFs and answers questions, explains technical terms, and simplifies dense passages. It pairs a LangChain RAG pipeline (PyPDF extraction, recursive chunking, sentence-transformer embeddings, FAISS vector store) with OpenAI chat completions so every response stays grounded in the source document.

## Architecture
- **Ingestion**: PDFs are uploaded via FastAPI, stored under `backend/storage/uploads`, and parsed with `pypdf`.
- **Chunking & Embeddings**: Text is split via a recursive splitter and embedded with `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector store**: Per-session FAISS indexes live in `backend/storage/sessions/<session_id>/faiss_index`.
- **LLM**: OpenAI chat completions (default `gpt-4o-mini`) generate answers using retrieved context; configure via environment variables.
- **Frontend**: A Vite + React client manages uploads, chat modes (Q&A, explain term, simplify), and displays cited chunks for transparency.

## Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
cp .env.example .env       # set OPENAI_API_KEY and optionally OPENAI_MODEL
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment knobs:
- `OPENAI_API_KEY` – **required**, authenticate with OpenAI.
- `OPENAI_MODEL` – override the chat model name (defaults to `gpt-4o-mini`).
- `EMBEDDING_MODEL_NAME` – change the embedding encoder.
- `MAX_CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K_RESULTS`, `MAX_COMPLETION_TOKENS` – tune RAG behaviour.

## Frontend setup
```bash
cd frontend
cp .env.example .env        # adjust API host if backend runs elsewhere
npm install
npm run dev
```

The dev server (port 5173) expects the FastAPI API at `VITE_API_BASE_URL` (defaults to `http://127.0.0.1:8000`).

## Typical flow
1. Upload a PDF. The backend extracts text, builds the FAISS index, and returns a `session_id`.
2. Ask questions or switch to “Explain term” / “Simplify” modes; responses cite the retrieved chunks.
3. Sessions persist on disk until manually removed—no cloud storage required.

## Future enhancements
- Swap in a stronger local LLM (TinyLlama, Phi-2, llama.cpp GGUF, etc.) when available.
- Surface PDF page thumbnails or outlines for faster navigation.
- Persist chat histories per session and support multi-document workspaces.
