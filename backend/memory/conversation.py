"""
Conversation memory — per-session message history stored in Redis.
Supports automatic compression via Gemini when history grows long.
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone

from google import genai
from google.genai import types

from backend.memory.redis_store import RedisStore

_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


class ConversationMemory:
    """
    Stores conversation messages in Redis.
    Key: conv_mem:{conversation_id}  →  Redis list of JSON messages
    """

    TTL = 86400       # 24 hours
    MAX_MESSAGES = 50  # hard cap before we force compression

    @staticmethod
    def _key(conversation_id: str) -> str:
        return f"conv_mem:{conversation_id}"

    @staticmethod
    async def add_message(
        conversation_id: str,
        role: str,           # "user" | "assistant" | "system"
        content: str,
        metadata: dict | None = None,
    ) -> None:
        """Append a message to the conversation history."""
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(metadata or {}),
        }
        await RedisStore.append_to_list(
            ConversationMemory._key(conversation_id),
            msg,
            max_length=ConversationMemory.MAX_MESSAGES,
            ttl_seconds=ConversationMemory.TTL,
        )

    @staticmethod
    async def get_history(conversation_id: str, last_n: int = 10) -> list[dict]:
        """Return the last N messages for context injection."""
        all_msgs = await RedisStore.get_list(ConversationMemory._key(conversation_id))
        return all_msgs[-last_n:] if len(all_msgs) > last_n else all_msgs

    @staticmethod
    async def get_all(conversation_id: str) -> list[dict]:
        return await RedisStore.get_list(ConversationMemory._key(conversation_id))

    @staticmethod
    async def clear(conversation_id: str) -> None:
        await RedisStore.delete(ConversationMemory._key(conversation_id))

    @staticmethod
    async def count(conversation_id: str) -> int:
        return await RedisStore.list_length(ConversationMemory._key(conversation_id))

    @staticmethod
    def _summarize_sync(history_text: str) -> str:
        client = _get_client()
        prompt = (
            "Summarize this conversation history concisely in 3–5 sentences. "
            "Preserve key facts, decisions, questions asked, and user intent. "
            "Write in third person (e.g., 'The user asked about...').\n\n"
            f"Conversation:\n{history_text}"
        )
        resp = client.models.generate_content(
            model=_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=256,
                temperature=0.1,
            ),
        )
        return (resp.text or "").strip()

    @staticmethod
    async def summarize_if_needed(
        conversation_id: str,
        threshold: int = 30,
    ) -> str | None:
        """
        If history length exceeds threshold, compress old messages into a summary.
        Replaces the list with [summary_message] + last 10 messages.
        Returns the summary text if compression occurred, otherwise None.
        """
        msgs = await ConversationMemory.get_all(conversation_id)
        if len(msgs) < threshold:
            return None

        # Build summary from all but the last 10
        to_compress = msgs[:-10]
        recent = msgs[-10:]

        history_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in to_compress
        )

        summary_text = await asyncio.to_thread(
            ConversationMemory._summarize_sync, history_text
        )

        summary_msg = {
            "role": "system",
            "content": f"[Conversation summary — earlier messages compressed]\n{summary_text}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compressed": True,
        }

        # Replace Redis list with summary + recent messages
        key = ConversationMemory._key(conversation_id)
        await RedisStore.delete(key)
        for msg in [summary_msg] + recent:
            await RedisStore.append_to_list(
                key,
                msg,
                max_length=ConversationMemory.MAX_MESSAGES,
                ttl_seconds=ConversationMemory.TTL,
            )

        return summary_text
