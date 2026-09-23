"""
In-process sliding-window rate limiter.

Limits are enforced per IP address using Redis if available, falling back
to an in-process dict.  Both chat and tasks endpoints are covered.

Defaults (configurable via environment variables):
  RATE_LIMIT_REQUESTS  — max requests per window  (default: 60)
  RATE_LIMIT_WINDOW_S  — window duration in seconds (default: 60)
"""
from __future__ import annotations

import os
import time
from collections import deque
from threading import Lock

_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
_WINDOW_S = int(os.getenv("RATE_LIMIT_WINDOW_S", "60"))

# Fallback in-process store: ip → deque of timestamps
_store: dict[str, deque] = {}
_lock = Lock()
_redis_client = None  # module-level sync Redis client (lazy-initialised)


class RateLimiter:
    """Sliding-window rate limiter (per-IP, in-process fallback)."""

    @staticmethod
    def is_allowed(ip: str, max_requests: int = _MAX_REQUESTS, window_s: int = _WINDOW_S) -> bool:
        """
        Returns True if the request is within rate limits, False if throttled.
        Uses Redis when available, falls back to in-process deque.
        """
        # Try Redis first (shared across workers)
        try:
            return RateLimiter._redis_check(ip, max_requests, window_s)
        except Exception:
            pass

        return RateLimiter._local_check(ip, max_requests, window_s)

    @staticmethod
    def _get_redis_client():
        """Return a module-level sync Redis client (created once, reused)."""
        global _redis_client
        if _redis_client is None:
            import redis as _redis
            from backend.memory.redis_store import _REDIS_URL, _REDIS_PASSWORD
            url = _REDIS_URL
            if _REDIS_PASSWORD and "@" not in url.split("://", 1)[-1]:
                scheme, rest = url.split("://", 1)
                url = f"{scheme}://:{_REDIS_PASSWORD}@{rest}"
            _redis_client = _redis.from_url(url, decode_responses=True)
        return _redis_client

    @staticmethod
    def _redis_check(ip: str, max_requests: int, window_s: int) -> bool:
        """Redis sliding-window using sorted set (score = timestamp)."""
        client = RateLimiter._get_redis_client()
        key = f"rl:{ip}"
        now = time.time()
        window_start = now - window_s

        pipe = client.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window_s + 1)
        results = pipe.execute()
        count = results[2]
        return count <= max_requests

    @staticmethod
    def _local_check(ip: str, max_requests: int, window_s: int) -> bool:
        """In-process deque-based sliding window."""
        now = time.time()
        window_start = now - window_s
        with _lock:
            if ip not in _store:
                _store[ip] = deque()
            q = _store[ip]
            # Evict expired timestamps
            while q and q[0] < window_start:
                q.popleft()
            if len(q) >= max_requests:
                return False
            q.append(now)
            return True

    @staticmethod
    def reset(ip: str) -> None:
        """Clear rate-limit state for an IP (for tests)."""
        with _lock:
            _store.pop(ip, None)
