from datetime import datetime, timezone
from time import struct_time

import feedparser
import httpx

from app.ingestion.collectors.base import BaseCollector
from app.ingestion.contracts import ArticleCandidate
from app.models.source import Source


class RSSCollector(BaseCollector):

    async def collect(self, source: Source) -> list[ArticleCandidate]:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=20.0,
        ) as client:
            response = await client.get(source.endpoint_url)
            response.raise_for_status()

        feed = feedparser.parse(response.content)

        candidates: list[ArticleCandidate] = []

        for entry in feed.entries:
            link = entry.get("link")
            title = entry.get("title")

            # These are required by ArticleCandidate.
            if not link or not title:
                continue

            candidate = ArticleCandidate(
                source_id=source.id,
                external_id=entry.get("id"),
                canonical_url=link,
                title=title,
                excerpt=entry.get("summary"),
                author=entry.get("author"),
                published_at=self._parse_published_at(
                    entry.get("published_parsed")
                ),
                raw_metadata={
                    "tags": [
                        tag.get("term")
                        for tag in entry.get("tags", [])
                        if tag.get("term")
                    ]
                },
            )

            candidates.append(candidate)

        return candidates

    @staticmethod
    def _parse_published_at(
        published_parsed: struct_time | None,
    ) -> datetime | None:

        if published_parsed is None:
            return None

        return datetime(
            published_parsed.tm_year,
            published_parsed.tm_mon,
            published_parsed.tm_mday,
            published_parsed.tm_hour,
            published_parsed.tm_min,
            published_parsed.tm_sec,
            tzinfo=timezone.utc,
        )