from abc import ABC, abstractmethod

from app.ingestion.contracts import ArticleCandidate
from app.models.source import Source


class BaseCollector(ABC):

    @abstractmethod
    async def collect(self, source: Source) -> list[ArticleCandidate]:
        pass