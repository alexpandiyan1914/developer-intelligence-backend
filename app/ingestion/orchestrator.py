from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.ingestion.collectors.rss import RSSCollector
from app.models.source import Source
from app.services.article_service import ArticleService


@dataclass
class IngestionResult:
    fetched: int
    created: int
    duplicates: int


class IngestionOrchestrator:

    def __init__(self):
        self.article_service = ArticleService()
        self.rss_collector = RSSCollector()

    async def ingest_rss_source(
        self,
        db: Session,
        source: Source,
    ) -> IngestionResult:

        candidates = await self.rss_collector.collect(source)

        created = 0
        duplicates = 0

        for candidate in candidates:
            _, was_created = self.article_service.ingest_candidate(
                db,
                candidate,
            )

            if was_created:
                created += 1
            else:
                duplicates += 1

        return IngestionResult(
            fetched=len(candidates),
            created=created,
            duplicates=duplicates,
        )