"""
Query analysis and rewriting.

Two strategies:
  1. Standalone query — if the user's message references prior context
     ("what about the second point?"), rewrite it as a self-contained query.
  2. Query expansion — add synonyms / related terms to improve recall for BM25.

Uses Gemini (same model as the answer layer) for rewriting.
"""
from __future__ import annotations

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client: genai.Client | None = None
_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

_REWRITE_PROMPT = """\
You are a query rewriting assistant. Given a conversation history and a new user query,
rewrite the query into a single, self-contained search query that captures the user's intent.

Rules:
- If the query is already clear and standalone, return it unchanged.
- Resolve pronouns and references to prior messages ("it", "that policy", "the second point").
- Keep the rewritten query concise (1-2 sentences max).
- Return ONLY the rewritten query — no explanation, no quotes.
"""


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def rewrite_query(
    query: str,
    conversation_history: list[dict] | None = None,
) -> str:
    """
    Rewrite query to be standalone. Returns the original query if no history
    or if the call fails (graceful degradation).
    """
    if not conversation_history:
        return query

    # Build a compact summary of recent conversation for context
    recent = conversation_history[-4:]  # last 2 turns
    history_text = "\n".join(
        f"{msg['role'].upper()}: {msg['content'][:300]}" for msg in recent
    )

    prompt = (
        f"Conversation so far:\n{history_text}\n\n"
        f"New user query: {query}\n\n"
        f"Rewritten standalone query:"
    )

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_REWRITE_PROMPT,
                max_output_tokens=128,
                temperature=0.0,
            ),
        )
        rewritten = (response.text or query).strip()
        return rewritten if rewritten else query
    except Exception:
        # Always fall back to original query — never break retrieval over rewriting
        return query
