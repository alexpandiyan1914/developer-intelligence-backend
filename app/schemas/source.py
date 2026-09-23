import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.db.enums import RegionCode, SourceCategory, SourceType


class SourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    slug: str = Field(min_length=1, max_length=160)

    source_type: SourceType
    source_category: SourceCategory
    default_region: RegionCode | None = None

    base_url: HttpUrl | None = None
    endpoint_url: HttpUrl

    enabled: bool = True

    fetch_interval_minutes: int = Field(
        default=60,
        gt=0,
    )

    reputation_weight: Decimal = Field(
        default=Decimal("0.5000"),
        ge=0,
        le=1,
    )

    config: dict[str, Any] = Field(default_factory=dict)


class SourceUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    source_category: SourceCategory | None = None
    default_region: RegionCode | None = None

    base_url: HttpUrl | None = None
    endpoint_url: HttpUrl | None = None

    enabled: bool | None = None

    fetch_interval_minutes: int | None = Field(
        default=None,
        gt=0,
    )

    reputation_weight: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    config: dict[str, Any] | None = None


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    name: str
    slug: str

    source_type: SourceType
    source_category: SourceCategory
    default_region: RegionCode | None

    base_url: str | None
    endpoint_url: str

    enabled: bool
    fetch_interval_minutes: int
    reputation_weight: Decimal

    config: dict[str, Any]

    last_attempt_at: datetime | None
    last_success_at: datetime | None

    created_at: datetime
    updated_at: datetime