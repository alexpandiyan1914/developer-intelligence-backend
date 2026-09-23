import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.source import Source


class SourceRepository:

    def create(
        self,
        db: Session,
        source: Source,
    ) -> Source:
        db.add(source)
        db.flush()
        db.refresh(source)

        return source

    def get_all(
        self,
        db: Session,
    ) -> list[Source]:
        statement = select(Source).order_by(
            Source.name.asc()
        )

        return list(
            db.scalars(statement).all()
        )

    def get_by_id(
        self,
        db: Session,
        source_id: uuid.UUID,
    ) -> Source | None:
        return db.get(Source, source_id)

    def get_by_slug(
        self,
        db: Session,
        slug: str,
    ) -> Source | None:
        statement = select(Source).where(
            Source.slug == slug
        )

        return db.scalar(statement)