import yaml
import os
from typing import List
from ..core.queue import QueueInterface, RedisQueue
from .registry import ScraperRegistry
from ..core.logging import logger
from ..core.tracing import generate_trace_id

class ScraperRouter:
    def __init__(self, config_path: str = "src/config/sources.yml"):
        self.config_path = config_path
        self.queue: QueueInterface = RedisQueue()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error("config_load_error", error=str(e))
            return {}

    async def dispatch_all(self):
        """
        Dispatch jobs for all registered and configured scrapers.
        """
        scrapers = ScraperRegistry.list_scrapers()
        
        for scraper_name in scrapers:
            if scraper_name in self.config:
                trace_id = generate_trace_id()
                job_payload = {
                    "scraper": scraper_name,
                    "config": self.config[scraper_name],
                    "trace_id": trace_id
                }
                
                msg_id = self.queue.push("ingestion_jobs", job_payload)
                logger.info("job_dispatched", scraper=scraper_name, msg_id=msg_id, trace_id=trace_id)
            else:
                logger.warning("scraper_not_configured", scraper=scraper_name)

router = ScraperRouter()
