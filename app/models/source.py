import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index

from app.db.base import Base
from app.db.enums import RegionCode, SourceCategory, SourceType


class Source(Base):
    __tablename__ = "sources"

    __table_args__ = (
    CheckConstraint(
        "fetch_interval_minutes > 0",
        name="ck_sources_fetch_interval_positive",
    ),
    CheckConstraint(
        "reputation_weight >= 0 AND reputation_weight <= 1",
        name="ck_sources_reputation_weight_range",
    ),
    Index(
        "idx_sources_enabled",
        "enabled",
    ),
    Index(
        "idx_sources_type_enabled",
        "source_type",
        "enabled",
    ),
)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
        unique=True,
    )

    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type"),
        nullable=False,
    )

    source_category: Mapped[SourceCategory] = mapped_column(
        Enum(SourceCategory, name="source_category"),
        nullable=False,
    )

    default_region: Mapped[RegionCode | None] = mapped_column(
        Enum(RegionCode, name="region_code"),
        nullable=True,
    )

    base_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    endpoint_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    fetch_interval_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=60,
        server_default="60",
    )

    reputation_weight: Mapped[float] = mapped_column(
        Numeric(5, 4),
        nullable=False,
        default=0.5000,
        server_default="0.5000",
    )

    http_etag: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    http_last_modified: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    config: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default="{}",
    )

    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_success_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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