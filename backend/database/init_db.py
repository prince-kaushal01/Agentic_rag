"""
Run this once to create all tables and the pgvector extension.
Usage: python -m backend.database.init_db
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


async def enable_pgvector():
    conn = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", 5433)),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    print("pgvector extension: OK")
    await conn.close()


async def create_tables():
    # import all models so metadata is populated
    from backend.database.models import (  # noqa: F401
        Organization, User, Document, DocumentChunk,
        Conversation, Message, Task, ToolCall,
        Approval, AuditLog,
    )
    from backend.database.connection import create_all_tables
    await create_all_tables()
    print("All tables created: OK")


async def main():
    print("Initialising database...")
    await enable_pgvector()
    await create_tables()
    print("\nDatabase ready.")


if __name__ == "__main__":
    asyncio.run(main())
