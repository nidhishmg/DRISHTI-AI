from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..schemas.models import Complaint

class BaseScraper(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def run(self) -> List[Complaint]:
        """
        Execute the scraping logic and return a list of Complaint objects.
        """
        pass

    @property
    @abstractmethod
    def source_type(self) -> str:
        """
        Return the source type identifier (e.g., 'youtube', 'twitter').
        """
        pass
