"""
Assembles retrieved chunks into a prompt-ready context block
and produces a structured source list for citations.
"""
from __future__ import annotations

from dataclasses import dataclass

from backend.retrieval.semantic import RetrievedChunk


@dataclass
class SourceCitation:
    chunk_id: str
    document_id: str
    file_name: str
    department: str | None
    section: str | None
    page_number: int | None
    score: float


@dataclass
class BuiltContext:
    context_text: str          # injected into the system prompt
    sources: list[SourceCitation]
    total_chars: int


def build_context(chunks: list[RetrievedChunk], max_chars: int = 12_000) -> BuiltContext:
    """
    Format retrieved chunks into a numbered context block.
    Truncates to max_chars to stay within LLM context limits.
    """
    if not chunks:
        return BuiltContext(
            context_text="No relevant documents found.",
            sources=[],
            total_chars=0,
        )

    sections: list[str] = []
    sources: list[SourceCitation] = []
    total = 0

    for i, chunk in enumerate(chunks, start=1):
        # Build a human-readable header for each chunk
        header_parts = [f"[{i}] {chunk.file_name}"]
        if chunk.section:
            header_parts.append(f"Section: {chunk.section}")
        if chunk.page_number:
            header_parts.append(f"Page {chunk.page_number}")
        if chunk.department:
            header_parts.append(f"Dept: {chunk.department}")
        header_parts.append(f"Relevance: {chunk.score:.2f}")

        header = " | ".join(header_parts)
        block = f"{header}\n{chunk.content}"

        if total + len(block) > max_chars:
            # Truncate the last chunk to fit
            remaining = max_chars - total
            if remaining > 200:
                block = block[:remaining] + "…"
                sections.append(block)
                total += len(block)
            break

        sections.append(block)
        total += len(block)

        sources.append(
            SourceCitation(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                file_name=chunk.file_name,
                department=chunk.department,
                section=chunk.section,
                page_number=chunk.page_number,
                score=chunk.score,
            )
        )

    context_text = "\n\n---\n\n".join(sections)
    return BuiltContext(context_text=context_text, sources=sources, total_chars=total)
