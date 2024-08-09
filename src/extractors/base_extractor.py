from abc import ABC, abstractmethod
from src.models.classes import Chapter, Novel

class BaseExtractor(ABC):
    @abstractmethod
    def extract_chapters(self, novel: Novel) -> list[Chapter]:
        pass