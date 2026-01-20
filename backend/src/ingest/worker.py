import asyncio
import json
from typing import Dict, Any
from ..core.queue import RedisQueue
from ..core.logging import logger
from ..core.tracing import set_trace_id, get_trace_id, TraceContext
from .registry import ScraperRegistry
# Ensure scrapers are registered
import src.ingest.scrapers

class IngestionWorker:
    def __init__(self):
        self.queue = RedisQueue()
        self.job_stream = "ingestion_jobs"
        self.data_stream = "complaint_events"
        self.group = "ingestion_workers"
        self.consumer = "worker_1" # In prod, unique ID

    async def process_job(self, msg_id: str, payload: Dict[str, Any]):
        trace_id = payload.get("trace_id")
        with TraceContext(trace_id):
            scraper_name = payload.get("scraper")
            config = json.loads(payload.get("config")) if isinstance(payload.get("config"), str) else payload.get("config")
            
            logger.info("processing_job", scraper=scraper_name, trace_id=trace_id)
            
            scraper_cls = ScraperRegistry.get_scraper(scraper_name)
            if not scraper_cls:
                logger.error("unknown_scraper", scraper=scraper_name)
                return

            try:
                scraper = scraper_cls(config)
                complaints = await scraper.run()
                
                for complaint in complaints:
                     # Ensure trace_id propagates
                    complaint.trace_id = get_trace_id()
                    
                    # Push standard complaint to data stream
                    self.queue.push(self.data_stream, complaint.model_dump(mode='json'))
                
                logger.info("job_completed", count=len(complaints))
            except Exception as e:
                logger.error("job_failed", error=str(e))

    async def run(self):
        logger.info("ingestion_worker_started")
        while True:
            try:
                # Read from generic job stream
                messages = self.queue.read_group(self.job_stream, self.group, self.consumer)
                for stream, msgs in messages:
                    for msg_id, data in msgs:
                        await self.process_job(msg_id, data)
                        self.queue.ack(stream, self.group, [msg_id])
                
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error("worker_loop_error", error=str(e))
                await asyncio.sleep(1)

if __name__ == "__main__":
    worker = IngestionWorker()
    asyncio.run(worker.run())
