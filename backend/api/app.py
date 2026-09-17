"""
FastAPI application factory.
Run with:  uvicorn backend.api.app:app --reload --port 8000
"""
from dotenv import load_dotenv
load_dotenv()  # load .env before any other imports that read env vars

import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.routes.chat import router as chat_router
from backend.api.routes.auth import router as auth_router
from backend.api.routes.tasks import router as tasks_router
from backend.api.routes.approvals import router as approvals_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="NovaTech Knowledge Assistant",
    description="Enterprise Agentic RAG — semantic search + LLM answers over company documents",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request timing middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    elapsed_ms = int((time.monotonic() - start) * 1000)
    response.headers["X-Process-Time-Ms"] = str(elapsed_ms)
    return response


# ── Rate limiting middleware ──────────────────────────────────────────────────
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Per-IP sliding-window rate limit on chat and tasks endpoints."""
    rate_limited_paths = ("/chat", "/tasks")
    if any(request.url.path.startswith(p) for p in rate_limited_paths):
        client_ip = (request.client.host if request.client else "unknown") or "unknown"
        try:
            from backend.security.rate_limiter import RateLimiter
            if not RateLimiter.is_allowed(client_ip):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Please slow down."},
                    headers={"Retry-After": "60"},
                )
        except Exception:
            pass  # fail open — never block on limiter errors
    return await call_next(request)


# ── Security middleware: prompt injection scan on incoming request body ────────
@app.middleware("http")
async def security_scan_middleware(request: Request, call_next):
    """Scan POST body for prompt injection attempts."""
    if request.method == "POST" and request.headers.get("content-type", "").startswith("application/json"):
        body_bytes: bytes = b""
        try:
            body_bytes = await request.body()
            if body_bytes:
                import json as _json
                body = _json.loads(body_bytes)
                query = body.get("query", "") or body.get("message", "")
                if query:
                    from backend.security.prompt_injection import PromptInjectionDefense
                    is_safe, threats = PromptInjectionDefense.is_safe_query(query)
                    if not is_safe:
                        logger.warning(
                            "Prompt injection detected in request to %s: %s",
                            request.url.path, threats,
                        )
                        return JSONResponse(
                            status_code=400,
                            content={
                                "error": "Query contains disallowed patterns",
                                "threats": threats,
                            },
                        )
        except Exception:
            pass  # never block on middleware errors — fail open

        # Re-inject the already-consumed body so downstream handlers can read it
        if body_bytes:
            async def receive() -> dict:
                return {"type": "http.request", "body": body_bytes, "more_body": False}
            request = Request(request.scope, receive)

    return await call_next(request)


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(tasks_router)
app.include_router(approvals_router)


# ── Health & info ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": "novatech-rag", "version": "1.0.0"}


@app.get("/tools", tags=["system"])
async def list_tools():
    """Return registered tool names and their risk levels."""
    from backend.tools.registry import TOOL_REGISTRY
    return {
        name: {"risk_level": meta["risk_level"], "timeout": meta["timeout"]}
        for name, meta in TOOL_REGISTRY.items()
    }


@app.get("/observability/costs", tags=["system"])
async def get_costs(tenant_id: str | None = None):
    """Return today's cost summary for a tenant (or whole system)."""
    try:
        from backend.observability.cost_tracker import CostTracker
        if tenant_id:
            data = await CostTracker.get_tenant_cost(tenant_id)
        else:
            data = {"message": "Provide ?tenant_id=<uuid> for tenant-scoped costs"}
        return data
    except Exception as e:
        return {"error": str(e)}


@app.get("/observability/models", tags=["system"])
async def get_models():
    """Return configured model names by tier."""
    from backend.observability.model_router import ModelRouter
    return ModelRouter.models()


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    import traceback
    tb = traceback.format_exc()
    logger.error("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__},
    )
