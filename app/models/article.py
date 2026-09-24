import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums import ArticleProcessingState


class Article(Base):
    __tablename__ = "articles"

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "canonical_url",
            name="uq_articles_source_canonical_url",
        ),
        Index(
            "idx_articles_source_published",
            "source_id",
            "published_at",
        ),
        Index(
            "idx_articles_processing_state",
            "processing_state",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sources.id"),
        nullable=False,
    )

    ingestion_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    story_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    canonical_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    excerpt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    community_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    community_comments: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    fingerprint: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    raw_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default="{}",
    )

    processing_state: Mapped[ArticleProcessingState] = mapped_column(
        Enum(
            ArticleProcessingState,
            name="article_processing_state",
        ),
        nullable=False,
        default=ArticleProcessingState.DISCOVERED,
        server_default=ArticleProcessingState.DISCOVERED.value,
    )

    processing_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )