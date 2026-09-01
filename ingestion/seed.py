"""
Seed the vector DB by ingesting all documents in the docs/ folder.
Usage: python -m ingestion.seed

Department → access_level mapping:
    hr, salary       → restricted
    finance, legal   → confidential
    engineering      → internal
    everything else  → internal
"""
import asyncio
import uuid
from pathlib import Path
from ingestion.pipeline import run_pipeline
from backend.database.connection import AsyncSessionLocal
from backend.database.models.users import Organization

DOCS_ROOT = Path(__file__).parent.parent / "Docs"

DEPARTMENT_MAP = {
    "hr":               ("hr",               "restricted"),
    "finance":          ("finance",           "confidential"),
    "legal":            ("legal",             "confidential"),
    "engineering":      ("engineering",       "internal"),
    "sales":            ("sales",             "internal"),
    "customer_support": ("customer_support",  "internal"),
    "marketing":        ("marketing",         "internal"),
    "operations":       ("operations",        "internal"),
}

SUPPORTED = {".md", ".txt", ".csv", ".pdf", ".docx", ".xlsx"}


async def get_or_create_tenant() -> uuid.UUID:
    """Return (or create) the NovaTech Solutions org record."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Organization).where(Organization.slug == "novatech")
        )
        org = result.scalar_one_or_none()
        if org is None:
            org = Organization(name="NovaTech Solutions", slug="novatech")
            session.add(org)
            await session.commit()
            await session.refresh(org)
            print(f"Created tenant: NovaTech Solutions ({org.id})")
        else:
            print(f"Tenant found: NovaTech Solutions ({org.id})")
        return org.id


async def main():
    print("=" * 60)
    print("NovaTech Solutions — Document Ingestion Seed")
    print("=" * 60)

    tenant_id = await get_or_create_tenant()

    files = [f for f in DOCS_ROOT.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED]
    print(f"\nFound {len(files)} documents to ingest\n")

    results = {"indexed": 0, "failed": 0, "total_chunks": 0}

    for file in sorted(files):
        # Determine department from parent folder name
        folder = file.parent.name.lower()
        department, access_level = DEPARTMENT_MAP.get(folder, (folder, "internal"))

        try:
            result = await run_pipeline(
                file,
                department=department,
                tenant_id=tenant_id,
                access_level=access_level,
            )
            if result.status == "indexed":
                results["indexed"] += 1
                results["total_chunks"] += result.chunks_indexed
            else:
                results["failed"] += 1
                print(f"  [FAIL] {file.name}: {result.error}")
        except Exception as e:
            results["failed"] += 1
            print(f"  [ERROR] {file.name}: {e}")

    print("\n" + "=" * 60)
    print(f"Ingestion complete")
    print(f"  Indexed : {results['indexed']} documents")
    print(f"  Failed  : {results['failed']} documents")
    print(f"  Chunks  : {results['total_chunks']} total in pgvector")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
