from sentence_transformers import SentenceTransformer
from ingestion.chunking.chunker import Chunk
import numpy as np

# Lightweight, fast model — swap to text-embedding-3-small via OpenAI for production
_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_chunks(chunks: list[Chunk], batch_size: int = 64) -> list[list[float]]:
    """
    Generate embeddings for a list of chunks.
    Returns list of float vectors (one per chunk).
    """
    model = _get_model()
    texts = [c.content for c in chunks]
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        normalize_embeddings=True,   # cosine similarity ready
        convert_to_numpy=True,
    )
    return [emb.tolist() for emb in embeddings]


def embed_query(query: str) -> list[float]:
    """Embed a single query string for retrieval."""
    model = _get_model()
    emb = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return emb.tolist()


def embedding_dimension() -> int:
    return _get_model().get_sentence_embedding_dimension()
