from pathlib import Path
from typing import Dict, List

from langchain_community.vectorstores import FAISS

from app import config
from app.services.embeddings import get_embedding_model
from app.services.llm import get_llm


class RAGPipeline:
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.llm = get_llm()

    def _load_vector_store(self, session_id: str) -> FAISS:
        session_dir = config.SESSION_DIR / session_id / "faiss_index"
        if not session_dir.exists():
            raise FileNotFoundError(f"Session {session_id} not found.")
        return FAISS.load_local(
            folder_path=str(session_dir),
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True,
        )

    def _format_prompt(self, context: str, question: str, mode: str) -> str:
        task_desc = {
            "qa": "Answer the question using the provided context.",
            "explain-term": "Explain the technical term in simple, precise language.",
            "simplify": "Rewrite the referenced section so that a graduate student can understand it.",
        }.get(mode, "Answer the question using the provided context.")

        return (
            "You are Paperpal, an assistant that reads research papers.\n"
            f"Task: {task_desc}\n"
            "Ground your response only on the context. Cite chunk numbers like [Chunk 2] when relevant.\n"
            "If the answer is not in the context, say so.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )

    def chat(self, session_id: str, question: str, mode: str = "qa") -> Dict:
        store = self._load_vector_store(session_id)
        docs = store.similarity_search(question, k=config.TOP_K_RESULTS)

        formatted_chunks: List[str] = []
        for idx, doc in enumerate(docs, start=1):
            formatted_chunks.append(f"[Chunk {idx}] {doc.page_content.strip()}")
        context = "\n\n".join(formatted_chunks)

        prompt = self._format_prompt(context=context, question=question, mode=mode)
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "chunks": formatted_chunks,
        }
