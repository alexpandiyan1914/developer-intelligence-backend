import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.ingestion.orchestrator import IngestionOrchestrator
from app.models.source import Source


async def main():
    db = SessionLocal()

    try:
        source = db.scalar(
            select(Source).where(
                Source.slug == "python-insider"
            )
        )

        if source is None:
            print("Source 'python-insider' not found.")
            return

        print("=== RSS INGESTION ===")
        print("Source:", source.name)
        print("Endpoint:", source.endpoint_url)

        orchestrator = IngestionOrchestrator()

        result = await orchestrator.ingest_rss_source(
            db,
            source,
        )

        print()
        print("=== RESULT ===")
        print("Fetched:", result.fetched)
        print("Created:", result.created)
        print("Duplicates:", result.duplicates)

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())