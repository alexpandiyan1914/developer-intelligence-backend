import uuid

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class ArticleCandidate(BaseModel):
    source_id: uuid.UUID

    external_id: str | None = None

    canonical_url: HttpUrl

    title: str = Field(
        min_length=1,
    )

    excerpt: str | None = None

    author: str | None = None

    published_at: datetime | None = None

    community_score: int | None = Field(
        default=None,
        ge=0,
    )

    community_comments: int | None = Field(
        default=None,
        ge=0,
    )

    raw_metadata: dict[str, Any] = Field(
        default_factory=dict,
    )