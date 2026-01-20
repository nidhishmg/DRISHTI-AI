from typing import Dict, Type, List
from .scraper import BaseScraper
from ..core.logging import logger

class ScraperRegistry:
    _registry: Dict[str, Type[BaseScraper]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(scraper_cls: Type[BaseScraper]):
            cls._registry[name] = scraper_cls
            logger.info("scraper_registered", name=name)
            return scraper_cls
        return decorator

    @classmethod
    def get_scraper(cls, name: str) -> Type[BaseScraper]:
        return cls._registry.get(name)

    @classmethod
    def list_scrapers(cls) -> List[str]:
        return list(cls._registry.keys())
