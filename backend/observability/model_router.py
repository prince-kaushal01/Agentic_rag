"""
Model router — selects the appropriate LLM model based on task complexity.

Strategy:
  - Classification / routing tasks (short, binary) → fast/cheap model
  - Standard retrieval + answer calls → primary model
  - Complex multi-step reasoning, long context → advanced model

Models are resolved from environment variables so they're easily swappable:
  LLM_MODEL_FAST    — classification & routing (default: gemini-2.0-flash)
  LLM_MODEL         — standard calls          (default: gemini-2.5-flash)
  LLM_MODEL_ADVANCED— complex reasoning       (default: gemini-2.5-pro)

Usage:
    from backend.observability.model_router import ModelRouter
    model = ModelRouter.select(task_type="classification", context_chars=0)
"""
from __future__ import annotations

import os
from enum import Enum

_MODEL_FAST = os.getenv("LLM_MODEL_FAST", "gemini-2.0-flash")
_MODEL_STANDARD = os.getenv("LLM_MODEL", "gemini-2.5-flash")
_MODEL_ADVANCED = os.getenv("LLM_MODEL_ADVANCED", "gemini-2.5-pro")

# Context size thresholds (characters)
_LONG_CONTEXT_THRESHOLD = 20_000   # above this → advanced model


class TaskType(str, Enum):
    classification = "classification"  # planner, router — short decisions
    retrieval_answer = "retrieval_answer"  # standard RAG answer
    summarization = "summarization"  # compress conversation history
    complex_reasoning = "complex_reasoning"  # multi-step analysis, long docs
    query_rewrite = "query_rewrite"  # lightweight query reformulation


class ModelRouter:
    """
    Selects the best-fit model for a given task type and context size.
    Never raises — falls back to the standard model on any error.
    """

    _TASK_MODEL_MAP: dict[TaskType, str] = {
        TaskType.classification: _MODEL_FAST,
        TaskType.retrieval_answer: _MODEL_STANDARD,
        TaskType.summarization: _MODEL_FAST,
        TaskType.complex_reasoning: _MODEL_ADVANCED,
        TaskType.query_rewrite: _MODEL_FAST,
    }

    @classmethod
    def select(
        cls,
        task_type: str | TaskType = TaskType.retrieval_answer,
        context_chars: int = 0,
        force_advanced: bool = False,
    ) -> str:
        """
        Return the model name string to use for this call.

        Args:
            task_type: The kind of LLM task being performed.
            context_chars: Total characters in the prompt context window.
            force_advanced: Override and always use the advanced model.
        """
        if force_advanced:
            return _MODEL_ADVANCED

        # Upgrade to advanced model for long contexts
        if context_chars >= _LONG_CONTEXT_THRESHOLD:
            return _MODEL_ADVANCED

        try:
            tt = TaskType(task_type) if isinstance(task_type, str) else task_type
            return cls._TASK_MODEL_MAP.get(tt, _MODEL_STANDARD)
        except (ValueError, KeyError):
            return _MODEL_STANDARD

    @classmethod
    def models(cls) -> dict[str, str]:
        """Return the currently configured model names."""
        return {
            "fast": _MODEL_FAST,
            "standard": _MODEL_STANDARD,
            "advanced": _MODEL_ADVANCED,
        }

    @classmethod
    def estimate_context_chars(cls, chunks: list, history: list) -> int:
        """
        Estimate total context size in characters.
        chunks: list of retrieval hits (must have .content or .text attribute)
        history: list of {"role": ..., "content": ...} dicts
        """
        chunk_chars = sum(
            len(getattr(c, "content", "") or getattr(c, "text", "") or "")
            for c in chunks
        )
        history_chars = sum(len(m.get("content", "")) for m in history)
        return chunk_chars + history_chars
