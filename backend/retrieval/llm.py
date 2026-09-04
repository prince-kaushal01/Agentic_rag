"""
LLM call layer — wraps Anthropic Claude.
Returns the answer text, token counts, and extracted citations.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

import anthropic

from backend.retrieval.context_builder import BuiltContext, SourceCitation

_client: anthropic.Anthropic | None = None

MODEL = os.getenv("LLM_MODEL", "claude-haiku-4-5-20251001")   # fast + cheap for RAG

# Cost per 1M tokens (USD) — update if model changes
_INPUT_COST_PER_M = 0.80
_OUTPUT_COST_PER_M = 4.00

SYSTEM_PROMPT = """\
You are a knowledgeable assistant for NovaTech Solutions employees.
Answer questions using ONLY the provided context documents.
Be concise and factual. When you use information from a document, cite it
with its reference number like [1], [2], etc.
If the answer is not in the context, say so clearly — do not guess or hallucinate.
"""


@dataclass
class LLMResponse:
    answer: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    model: str
    cited_indices: list[int] = field(default_factory=list)   # 1-based refs found in answer


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _extract_citations(text: str) -> list[int]:
    """Pull [1], [2] … reference numbers from the answer."""
    return sorted({int(m) for m in re.findall(r"\[(\d+)\]", text)})


def answer_with_context(
    query: str,
    context: BuiltContext,
    conversation_history: list[dict] | None = None,
) -> LLMResponse:
    """
    Call Claude with the retrieved context and return a structured response.

    conversation_history: list of {"role": "user"|"assistant", "content": str}
    """
    client = _get_client()

    # Build the user turn: context block + question
    user_content = (
        f"## Relevant Documents\n\n{context.context_text}\n\n"
        f"## Question\n\n{query}"
    )

    messages: list[dict] = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_content})

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    answer = response.content[0].text
    input_tok = response.usage.input_tokens
    output_tok = response.usage.output_tokens
    cost = (input_tok / 1_000_000 * _INPUT_COST_PER_M) + (
        output_tok / 1_000_000 * _OUTPUT_COST_PER_M
    )

    return LLMResponse(
        answer=answer,
        input_tokens=input_tok,
        output_tokens=output_tok,
        cost_usd=round(cost, 6),
        model=MODEL,
        cited_indices=_extract_citations(answer),
    )
