import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.source import Source
from app.repositories.source_repository import SourceRepository
from app.schemas.source import SourceCreate


class SourceService:

    def __init__(self):
        self.repository = SourceRepository()

    def create_source(
        self,
        db: Session,
        data: SourceCreate,
    ) -> Source:

        existing_source = self.repository.get_by_slug(
            db,
            data.slug,
        )

        if existing_source is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Source slug already exists",
            )

        source = Source(
            name=data.name,
            slug=data.slug,
            source_type=data.source_type,
            source_category=data.source_category,
            default_region=data.default_region,
            base_url=str(data.base_url) if data.base_url else None,
            endpoint_url=str(data.endpoint_url),
            enabled=data.enabled,
            fetch_interval_minutes=data.fetch_interval_minutes,
            reputation_weight=data.reputation_weight,
            config=data.config,
        )

        try:
            self.repository.create(db, source)
            db.commit()
            db.refresh(source)

            return source

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Source conflicts with an existing record",
            )

    def get_sources(
        self,
        db: Session,
    ) -> list[Source]:
        return self.repository.get_all(db)

    def get_source(
        self,
        db: Session,
        source_id: uuid.UUID,
    ) -> Source:

        source = self.repository.get_by_id(
            db,
            source_id,
        )

        if source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found",
            )

        return source