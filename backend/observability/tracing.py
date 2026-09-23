"""
Request tracing — lightweight span-based tracer that writes to Redis and
optionally forwards to an OTLP endpoint (e.g. Langfuse, Jaeger, Grafana Tempo).

No external dependency required for basic operation; OTLP export is attempted
only when OTLP_ENDPOINT is set in the environment.

Usage:
    tracer = get_tracer("chat")
    with tracer.start_span("hybrid_search", attributes={"query": query}) as span:
        result = await hybrid_search(...)
        span.set_attribute("chunks_returned", len(result))
"""
from __future__ import annotations

import json
import logging
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Generator

logger = logging.getLogger(__name__)

_OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT")      # e.g. http://localhost:4318/v1/traces
_SERVICE_NAME = os.getenv("SERVICE_NAME", "novatech-rag")


@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_span_id: str | None
    name: str
    service: str
    start_time_ms: float
    end_time_ms: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "ok"           # "ok" | "error"
    error_message: str | None = None

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def set_error(self, message: str) -> None:
        self.status = "error"
        self.error_message = message

    def finish(self) -> None:
        self.end_time_ms = time.monotonic() * 1000

    @property
    def duration_ms(self) -> float:
        if self.end_time_ms is None:
            return 0.0
        return self.end_time_ms - self.start_time_ms

    def to_dict(self) -> dict:
        d = asdict(self)
        d["duration_ms"] = self.duration_ms
        return d


class Tracer:
    """Lightweight span tracer for a named service component."""

    def __init__(self, component: str, service: str = _SERVICE_NAME):
        self._component = component
        self._service = service

    def start_span(
        self,
        name: str,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        attributes: dict | None = None,
    ) -> "SpanContext":
        span = Span(
            trace_id=trace_id or str(uuid.uuid4()),
            span_id=str(uuid.uuid4()),
            parent_span_id=parent_span_id,
            name=f"{self._component}.{name}",
            service=self._service,
            start_time_ms=time.monotonic() * 1000,
            attributes=attributes or {},
        )
        return SpanContext(span)


class SpanContext:
    """Context manager that finishes the span on exit and emits it."""

    def __init__(self, span: Span):
        self.span = span

    def set_attribute(self, key: str, value: Any) -> None:
        self.span.set_attribute(key, value)

    def set_error(self, message: str) -> None:
        self.span.set_error(message)

    def __enter__(self) -> "SpanContext":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.span.finish()
        if exc_type is not None:
            self.span.set_error(str(exc_val))
        _emit_span(self.span)
        return False  # don't suppress exceptions


def _emit_span(span: Span) -> None:
    """Emit a finished span to Redis (for inspection) and optionally OTLP."""
    try:
        _emit_to_redis(span)
    except Exception:
        pass

    if _OTLP_ENDPOINT:
        try:
            _emit_to_otlp(span)
        except Exception:
            pass


_sync_redis_client = None  # module-level sync client — created once, reused


def _get_sync_redis():
    global _sync_redis_client
    if _sync_redis_client is None:
        import redis as _redis
        from backend.memory.redis_store import _REDIS_URL, _REDIS_PASSWORD
        url = _REDIS_URL
        if _REDIS_PASSWORD and "@" not in url.split("://", 1)[-1]:
            scheme, rest = url.split("://", 1)
            url = f"{scheme}://:{_REDIS_PASSWORD}@{rest}"
        _sync_redis_client = _redis.from_url(url, decode_responses=True)
    return _sync_redis_client


def _emit_to_redis(span: Span) -> None:
    """Store span in Redis sorted set keyed by trace_id."""
    client = _get_sync_redis()
    key = f"trace:{span.trace_id}"
    client.zadd(key, {json.dumps(span.to_dict()): span.start_time_ms})
    client.expire(key, 3600)  # 1 hour TTL


def _emit_to_otlp(span: Span) -> None:
    """Forward span to an OTLP HTTP endpoint (best-effort)."""
    import urllib.request

    payload = {
        "resourceSpans": [{
            "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": span.service}}]},
            "scopeSpans": [{
                "spans": [{
                    "traceId": span.trace_id.replace("-", ""),
                    "spanId": span.span_id.replace("-", "")[:16],
                    "name": span.name,
                    "startTimeUnixNano": int(span.start_time_ms * 1_000_000),
                    "endTimeUnixNano": int((span.end_time_ms or span.start_time_ms) * 1_000_000),
                    "status": {"code": 2 if span.status == "error" else 1},
                    "attributes": [
                        {"key": k, "value": {"stringValue": str(v)}}
                        for k, v in span.attributes.items()
                    ],
                }]
            }]
        }]
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        _OTLP_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=2)


# ── Public helpers ─────────────────────────────────────────────────────────────

def get_tracer(component: str) -> Tracer:
    """Return a tracer for the given component name."""
    return Tracer(component)


async def trace_request(
    component: str,
    operation: str,
    attributes: dict | None = None,
) -> SpanContext:
    """Convenience: return an open SpanContext for use in async code."""
    tracer = get_tracer(component)
    return tracer.start_span(operation, attributes=attributes)


def get_trace(trace_id: str) -> list[dict]:
    """Retrieve all spans for a trace_id from Redis (for debugging)."""
    try:
        client = _get_sync_redis()
        raw = client.zrange(f"trace:{trace_id}", 0, -1)
        return [json.loads(r) for r in raw]
    except Exception:
        return []
