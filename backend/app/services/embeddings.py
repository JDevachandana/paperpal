from functools import lru_cache

from langchain_community.embeddings import SentenceTransformerEmbeddings

from app import config


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformerEmbeddings:
    """Singleton embedding model to avoid reloading on every request."""
    return SentenceTransformerEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
