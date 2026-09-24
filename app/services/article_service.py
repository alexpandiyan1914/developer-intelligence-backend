from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ingestion.contracts import ArticleCandidate
from app.models.article import Article
from app.repositories.article_repository import ArticleRepository


class ArticleService:

    def __init__(self):
        self.repository = ArticleRepository()

    def ingest_candidate(
        self,
        db: Session,
        candidate: ArticleCandidate,
    ) -> tuple[Article, bool]:

        canonical_url = str(candidate.canonical_url)

        # First duplicate check:
        # Has this source already stored this exact URL?
        existing_article = self.repository.get_by_source_and_url(
            db,
            candidate.source_id,
            canonical_url,
        )

        if existing_article is not None:
            return existing_article, False

        # Some sources also provide their own stable ID.
        if candidate.external_id is not None:
            existing_article = self.repository.get_by_external_id(
                db,
                candidate.source_id,
                candidate.external_id,
            )

            if existing_article is not None:
                return existing_article, False

        article = Article(
            source_id=candidate.source_id,
            external_id=candidate.external_id,
            canonical_url=canonical_url,
            title=candidate.title,
            excerpt=candidate.excerpt,
            author=candidate.author,
            published_at=candidate.published_at,
            community_score=candidate.community_score,
            community_comments=candidate.community_comments,
            raw_metadata=candidate.raw_metadata,
        )

        try:
            self.repository.create(
                db,
                article,
            )

            db.commit()
            db.refresh(article)

            return article, True

        except IntegrityError:
            db.rollback()
            raise