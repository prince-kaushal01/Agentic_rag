"""
FastAPI application factory.
Run with:  uvicorn backend.api.app:app --reload --port 8000
"""
from dotenv import load_dotenv
load_dotenv()  # load .env before any other imports that read env vars

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.chat import router as chat_router
from backend.api.routes.auth import router as auth_router

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

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "novatech-rag"}


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    import traceback
    tb = traceback.format_exc()
    return __import__("fastapi").responses.JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__, "traceback": tb},
    )
