import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
SESSION_DIR = STORAGE_DIR / "sessions"

# Model choices are intentionally lightweight so the project remains runnable
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_COMPLETION_TOKENS = int(os.getenv("MAX_COMPLETION_TOKENS", 400))

MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 4))


for directory in (STORAGE_DIR, UPLOAD_DIR, SESSION_DIR):
    directory.mkdir(parents=True, exist_ok=True)
