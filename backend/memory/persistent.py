"""
Persistent memory — user preferences and explicitly saved facts.
Stored in Redis with no TTL (durable across sessions).
"""
from __future__ import annotations

import json

from backend.memory.redis_store import RedisStore


class PersistentMemory:
    """
    User-scoped memory that persists indefinitely.
    Key: persistent_prefs:{user_id}   → Redis hash (field → value)
         persistent_facts:{user_id}   → Redis list of fact strings
    """

    @staticmethod
    def _prefs_key(user_id: str) -> str:
        return f"persistent_prefs:{user_id}"

    @staticmethod
    def _facts_key(user_id: str) -> str:
        return f"persistent_facts:{user_id}"

    @staticmethod
    async def save_preference(user_id: str, key: str, value: str) -> None:
        """Save a named preference for a user (e.g., timezone, language)."""
        await RedisStore.set_hash_field(PersistentMemory._prefs_key(user_id), key, value)

    @staticmethod
    async def get_preferences(user_id: str) -> dict[str, str]:
        """Return all saved preferences for a user."""
        return await RedisStore.get_hash(PersistentMemory._prefs_key(user_id))

    @staticmethod
    async def save_fact(user_id: str, fact: str) -> None:
        """Explicitly save a fact the user wants remembered across sessions."""
        await RedisStore.append_to_list(
            PersistentMemory._facts_key(user_id),
            {"fact": fact},
            max_length=100,
            ttl_seconds=0,  # no expiry
        )

    @staticmethod
    async def get_facts(user_id: str) -> list[str]:
        """Retrieve all saved facts for a user."""
        items = await RedisStore.get_list(PersistentMemory._facts_key(user_id))
        return [item.get("fact", "") for item in items if item.get("fact")]

    @staticmethod
    async def delete_fact(user_id: str, fact_index: int) -> bool:
        """
        Delete a fact by index (0-based).
        Returns True if deleted, False if index out of range.
        """
        facts = await PersistentMemory.get_facts(user_id)
        if fact_index < 0 or fact_index >= len(facts):
            return False

        # Rebuild list without the deleted fact
        remaining = [f for i, f in enumerate(facts) if i != fact_index]
        key = PersistentMemory._facts_key(user_id)
        await RedisStore.delete(key)
        for f in remaining:
            await RedisStore.append_to_list(
                key,
                {"fact": f},
                max_length=100,
                ttl_seconds=0,
            )
        return True

    @staticmethod
    async def clear_all(user_id: str) -> None:
        """Clear all persistent memory for a user (GDPR erasure support)."""
        await RedisStore.delete(PersistentMemory._prefs_key(user_id))
        await RedisStore.delete(PersistentMemory._facts_key(user_id))
