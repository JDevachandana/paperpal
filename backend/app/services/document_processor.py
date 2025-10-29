import json
import uuid
from pathlib import Path
from typing import List

from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader

from app import config
from app.services.embeddings import get_embedding_model


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.MAX_CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self.embedding_model = get_embedding_model()

    def create_session(self) -> str:
        session_id = uuid.uuid4().hex
        session_dir = config.SESSION_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_id

    def save_upload(self, upload: UploadFile, session_id: str) -> Path:
        file_extension = Path(upload.filename or "paper.pdf").suffix or ".pdf"
        target_path = config.UPLOAD_DIR / f"{session_id}{file_extension}"
        with target_path.open("wb") as destination:
            content = upload.file.read()
            destination.write(content)
        return target_path

    def _extract_text(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        pages: List[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text.strip())
        return "\n\n".join(pages)

    def build_vector_store(self, session_id: str, raw_text: str) -> dict:
        if not raw_text.strip():
            raise ValueError("Uploaded PDF does not contain extractable text.")

        chunks = self.text_splitter.split_text(raw_text)
        faiss_store = FAISS.from_texts(chunks, embedding=self.embedding_model)
        session_dir = config.SESSION_DIR / session_id
        index_dir = session_dir / "faiss_index"
        faiss_store.save_local(str(index_dir))

        meta = {
            "chunk_count": len(chunks),
            "character_count": len(raw_text),
            "session_id": session_id,
        }

        with (session_dir / "meta.json").open("w") as f:
            json.dump(meta, f, indent=2)

        return meta

    def process_upload(self, upload: UploadFile) -> dict:
        session_id = self.create_session()
        file_path = self.save_upload(upload, session_id)
        raw_text = self._extract_text(file_path)
        stats = self.build_vector_store(session_id, raw_text)
        stats["filename"] = upload.filename
        return stats
