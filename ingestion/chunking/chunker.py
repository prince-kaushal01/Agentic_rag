from dataclasses import dataclass, field
from ingestion.parsers.base import ParsedDocument
import re


@dataclass
class Chunk:
    """A single chunk ready for embedding + indexing."""
    chunk_index: int
    content: str
    section: str = ""
    page_number: int | None = None
    token_count: int = 0
    metadata: dict = field(default_factory=dict)


def _estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 4 characters."""
    return max(1, len(text) // 4)


def _split_text(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    """Split text into overlapping windows by sentence boundaries."""
    sentences = re.split(r"(?<=[.!?])\s+|\n{2,}", text.strip())
    chunks = []
    current: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        s_tokens = _estimate_tokens(sentence)

        if current_tokens + s_tokens > max_tokens and current:
            chunks.append(" ".join(current))
            # keep overlap: drop sentences from front until under overlap budget
            while current and current_tokens > overlap_tokens:
                removed = current.pop(0)
                current_tokens -= _estimate_tokens(removed)

        current.append(sentence)
        current_tokens += s_tokens

    if current:
        chunks.append(" ".join(current))

    return [c for c in chunks if c.strip()]


def chunk_document(
    doc: ParsedDocument,
    max_tokens: int = 400,
    overlap_tokens: int = 80,
) -> list[Chunk]:
    """
    Strategy:
    - If document has sections → chunk per section (respects structure).
    - If document has pages    → chunk per page.
    - Fallback                 → chunk full content.
    Each logical unit is further split if it exceeds max_tokens.
    """
    chunks: list[Chunk] = []
    idx = 0

    def add_chunks(text: str, section: str = "", page: int | None = None):
        nonlocal idx
        for piece in _split_text(text, max_tokens, overlap_tokens):
            chunks.append(Chunk(
                chunk_index=idx,
                content=piece,
                section=section,
                page_number=page,
                token_count=_estimate_tokens(piece),
                metadata={"file_name": doc.file_name, "file_type": doc.file_type},
            ))
            idx += 1

    if doc.sections:
        for sec in doc.sections:
            add_chunks(sec["text"], section=sec["title"])
    elif doc.pages:
        for pg in doc.pages:
            add_chunks(pg["text"], page=pg["page"])
    else:
        add_chunks(doc.content)

    return chunks
