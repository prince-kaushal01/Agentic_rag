"""
Cost tracker — accumulates LLM token costs per conversation, task, and user.
Persists aggregates in Redis with daily roll-up buckets.

Supported models and their pricing (USD per 1K tokens):
  - gemini-2.5-flash : input=$0.000075, output=$0.0003
  - gemini-2.0-flash : input=$0.000075, output=$0.0003
  - gemini-1.5-flash : input=$0.000075, output=$0.0003

Values are kept in sync with pricing at module import; override via env vars:
  COST_INPUT_PER_1K  — input token cost per 1K tokens
  COST_OUTPUT_PER_1K — output token cost per 1K tokens
"""
from __future__ import annotations

import json
import os
import time
from datetime import date, datetime, timezone
from typing import Optional

_INPUT_COST_PER_1K = float(os.getenv("COST_INPUT_PER_1K", "0.000075"))
_OUTPUT_COST_PER_1K = float(os.getenv("COST_OUTPUT_PER_1K", "0.0003"))

# Pricing table for known models (USD / 1K tokens)
_MODEL_PRICING: dict[str, tuple[float, float]] = {
    "gemini-2.5-flash":       (0.000075, 0.0003),
    "gemini-2.0-flash":       (0.000075, 0.0003),
    "gemini-1.5-flash":       (0.000075, 0.0003),
    "gemini-1.5-pro":         (0.00125,  0.005),
    "gemini-2.5-pro":         (0.00125,  0.005),
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gemini-2.5-flash",
) -> float:
    """Return the USD cost for a single LLM call."""
    input_rate, output_rate = _MODEL_PRICING.get(model, (_INPUT_COST_PER_1K, _OUTPUT_COST_PER_1K))
    return (input_tokens * input_rate + output_tokens * output_rate) / 1000.0


class CostTracker:
    """
    Tracks LLM spend across dimensions: conversation, task, user, and tenant.

    All data is stored in Redis hashes with daily key buckets so you can
    query spend per day, per user, and per tenant.

    Key schema:
        cost:conv:{conversation_id}   → hash: total_usd, input_tokens, output_tokens, calls
        cost:task:{task_id}           → hash: total_usd, input_tokens, output_tokens, calls
        cost:user:{user_id}:{date}    → hash: total_usd, input_tokens, output_tokens, calls
        cost:tenant:{tenant_id}:{date}→ hash: total_usd, input_tokens, output_tokens, calls
    """

    CONV_TTL = 7 * 86400    # 7 days
    TASK_TTL = 7 * 86400
    USER_TTL = 30 * 86400   # 30 days
    TENANT_TTL = 90 * 86400 # 90 days

    @staticmethod
    def _today() -> str:
        return date.today().isoformat()

    @classmethod
    async def record(
        cls,
        *,
        input_tokens: int,
        output_tokens: int,
        model: str = "gemini-2.5-flash",
        conversation_id: Optional[str] = None,
        task_id: Optional[str] = None,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> float:
        """
        Record a single LLM call's cost across all relevant dimensions.
        Returns the USD cost for this call.
        """
        cost_usd = calculate_cost(input_tokens, output_tokens, model)
        today = cls._today()

        try:
            import redis.asyncio as aioredis
            from backend.memory.redis_store import _REDIS_URL
            client = aioredis.from_url(_REDIS_URL, decode_responses=True)

            pipe = client.pipeline()

            def _incr(key: str, ttl: int) -> None:
                pipe.hincrbyfloat(key, "total_usd", cost_usd)
                pipe.hincrby(key, "input_tokens", input_tokens)
                pipe.hincrby(key, "output_tokens", output_tokens)
                pipe.hincrby(key, "calls", 1)
                pipe.expire(key, ttl)

            if conversation_id:
                _incr(f"cost:conv:{conversation_id}", cls.CONV_TTL)
            if task_id:
                _incr(f"cost:task:{task_id}", cls.TASK_TTL)
            if user_id:
                _incr(f"cost:user:{user_id}:{today}", cls.USER_TTL)
            if tenant_id:
                _incr(f"cost:tenant:{tenant_id}:{today}", cls.TENANT_TTL)

            await pipe.execute()
        except Exception:
            pass  # non-critical — never block on cost tracking failures

        return cost_usd

    @classmethod
    async def get_conversation_cost(cls, conversation_id: str) -> dict:
        """Return cost summary for a conversation."""
        return await cls._get_hash(f"cost:conv:{conversation_id}")

    @classmethod
    async def get_task_cost(cls, task_id: str) -> dict:
        """Return cost summary for a task."""
        return await cls._get_hash(f"cost:task:{task_id}")

    @classmethod
    async def get_user_cost(cls, user_id: str, day: str | None = None) -> dict:
        """Return cost summary for a user on a given day (default: today)."""
        return await cls._get_hash(f"cost:user:{user_id}:{day or cls._today()}")

    @classmethod
    async def get_tenant_cost(cls, tenant_id: str, day: str | None = None) -> dict:
        """Return cost summary for a tenant on a given day (default: today)."""
        return await cls._get_hash(f"cost:tenant:{tenant_id}:{day or cls._today()}")

    @staticmethod
    async def _get_hash(key: str) -> dict:
        try:
            import redis.asyncio as aioredis
            from backend.memory.redis_store import _REDIS_URL
            client = aioredis.from_url(_REDIS_URL, decode_responses=True)
            data = await client.hgetall(key)
            return {
                "total_usd": float(data.get("total_usd", 0)),
                "input_tokens": int(data.get("input_tokens", 0)),
                "output_tokens": int(data.get("output_tokens", 0)),
                "calls": int(data.get("calls", 0)),
            }
        except Exception:
            return {"total_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "calls": 0}
