"""
Redis store wrapper — async Redis operations used by all memory layers.
"""
from __future__ import annotations

import json
import os

import redis.asyncio as aioredis

from dotenv import load_dotenv

load_dotenv()

_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
_REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

_client: aioredis.Redis | None = None


class RedisStore:
    """Singleton async Redis client with JSON serialization helpers."""

    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        global _client
        if _client is None:
            url = _REDIS_URL
            if _REDIS_PASSWORD and "://:@" not in url and "@" not in url.split("://", 1)[-1]:
                # inject password into URL if not already present
                scheme, rest = url.split("://", 1)
                url = f"{scheme}://:{_REDIS_PASSWORD}@{rest}"
            _client = aioredis.from_url(url, decode_responses=True)
        return _client

    @classmethod
    async def set(cls, key: str, value: dict, ttl_seconds: int = 3600) -> None:
        client = await cls.get_client()
        if ttl_seconds > 0:
            await client.setex(key, ttl_seconds, json.dumps(value))
        else:
            await client.set(key, json.dumps(value))

    @classmethod
    async def get(cls, key: str) -> dict | None:
        client = await cls.get_client()
        data = await client.get(key)
        return json.loads(data) if data else None

    @classmethod
    async def delete(cls, key: str) -> None:
        client = await cls.get_client()
        await client.delete(key)

    @classmethod
    async def append_to_list(
        cls,
        key: str,
        item: dict,
        max_length: int = 100,
        ttl_seconds: int = 3600,
    ) -> None:
        """Append a JSON item to a Redis list, trim to max_length, and refresh TTL."""
        client = await cls.get_client()
        await client.rpush(key, json.dumps(item))
        await client.ltrim(key, -max_length, -1)
        if ttl_seconds > 0:
            await client.expire(key, ttl_seconds)

    @classmethod
    async def get_list(cls, key: str) -> list[dict]:
        client = await cls.get_client()
        items = await client.lrange(key, 0, -1)
        return [json.loads(i) for i in items]

    @classmethod
    async def list_length(cls, key: str) -> int:
        client = await cls.get_client()
        return await client.llen(key)

    @classmethod
    async def set_hash_field(cls, key: str, field: str, value: str, ttl_seconds: int = 0) -> None:
        client = await cls.get_client()
        await client.hset(key, field, value)
        if ttl_seconds > 0:
            await client.expire(key, ttl_seconds)

    @classmethod
    async def get_hash(cls, key: str) -> dict[str, str]:
        client = await cls.get_client()
        return await client.hgetall(key)
