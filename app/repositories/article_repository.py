import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import Article


class ArticleRepository:

    def create(
        self,
        db: Session,
        article: Article,
    ) -> Article:

        db.add(article)
        db.flush()
        db.refresh(article)

        return article

    def get_by_id(
        self,
        db: Session,
        article_id: uuid.UUID,
    ) -> Article | None:

        return db.get(
            Article,
            article_id,
        )

    def get_by_source_and_url(
        self,
        db: Session,
        source_id: uuid.UUID,
        canonical_url: str,
    ) -> Article | None:

        statement = select(Article).where(
            Article.source_id == source_id,
            Article.canonical_url == canonical_url,
        )

        return db.scalar(statement)

    def get_by_external_id(
        self,
        db: Session,
        source_id: uuid.UUID,
        external_id: str,
    ) -> Article | None:

        statement = select(Article).where(
            Article.source_id == source_id,
            Article.external_id == external_id,
        )

        return db.scalar(statement)