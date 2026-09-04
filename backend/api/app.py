"""
FastAPI application factory.
Run with:  uvicorn backend.api.app:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.chat import router as chat_router

app = FastAPI(
    title="NovaTech Knowledge Assistant",
    description="Enterprise Agentic RAG — semantic search + LLM answers over company documents",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "novatech-rag"}
