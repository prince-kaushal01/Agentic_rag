"""
LLM call layer — wraps Google Gemini via google-genai SDK.
Returns the answer text, token counts, and extracted citations.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from google import genai
from google.genai import types
from dotenv import load_dotenv

from backend.retrieval.context_builder import BuiltContext
from backend.observability.cost_tracker import calculate_cost

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """\
You are a knowledgeable assistant for NovaTech Solutions employees.
Answer questions using ONLY the provided context documents.
Be concise and factual. When you use information from a document, cite it
with its reference number like [1], [2], etc.
If the answer is not in the context, say so clearly — do not guess or hallucinate.
"""

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def _extract_citations(text: str) -> list[int]:
    """Pull [1], [2] … reference numbers from the answer."""
    return sorted({int(m) for m in re.findall(r"\[(\d+)\]", text)})


@dataclass
class LLMResponse:
    answer: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    model: str
    cited_indices: list[int] = field(default_factory=list)


def answer_with_context(
    query: str,
    context: BuiltContext,
    conversation_history: list[dict] | None = None,
) -> LLMResponse:
    """
    Call Gemini with the retrieved context and return a structured response.

    conversation_history: list of {"role": "user"|"model", "content": str}
    """
    client = _get_client()

    # Build the user turn: context block + question
    user_content = (
        f"## Relevant Documents\n\n{context.context_text}\n\n"
        f"## Question\n\n{query}"
    )

    # Build message history for multi-turn
    contents: list[types.Content] = []
    if conversation_history:
        for msg in conversation_history:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    contents.append(types.Content(role="user", parts=[types.Part(text=user_content)]))

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1024,
            temperature=0.2,
        ),
    )

    answer = response.text or ""
    input_tok = response.usage_metadata.prompt_token_count or 0
    output_tok = response.usage_metadata.candidates_token_count or 0
    cost = calculate_cost(input_tok, output_tok, MODEL)

    return LLMResponse(
        answer=answer,
        input_tokens=input_tok,
        output_tokens=output_tok,
        cost_usd=round(cost, 6),
        model=MODEL,
        cited_indices=_extract_citations(answer),
    )
