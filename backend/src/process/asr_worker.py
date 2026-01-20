import asyncio
import hashlib
from typing import Dict, Any, Optional
from ..core.queue import RedisQueue
from ..core.logging import logger
from ..config.settings import get_settings
from .audio import WhisperAudioProcessor

settings = get_settings()

class ASRWorker:
    def __init__(self):
        self.queue = RedisQueue()
        self.job_stream = "asr_jobs"
        self.group = "asr_workers"
        self.consumer = "asr_worker_1"
        self.processor = WhisperAudioProcessor()
        self.semaphore = asyncio.Semaphore(settings.ASR_CONCURRENCY_LIMIT)
        
        # Simple in-memory cache for demo (LRU in prod)
        self.cache: Dict[str, Dict] = {}

    def get_cache_key(self, file_path: str) -> str:
        # specific to file path + model
        return hashlib.md5(f"{file_path}:{settings.WHISPER_MODEL}".encode()).hexdigest()

    async def process_job(self, msg_id: str, payload: Dict[str, Any]):
        file_path = payload.get("file_path")
        trace_id = payload.get("trace_id")
        
        cache_key = self.get_cache_key(file_path)
        
        # Check Cache
        if cache_key in self.cache:
            logger.info("asr_cache_hit", trace_id=trace_id)
            result = self.cache[cache_key]
            # Emit result
            self.queue.push("asr_results", {**result, "trace_id": trace_id, "status": "completed"})
            return

        async with self.semaphore:
            try:
                logger.info("asr_start", trace_id=trace_id, file=file_path)
                # Run CPU/GPU bound task in thread pool
                result = await asyncio.to_thread(self.processor.predict, file_path)
                
                # Update Cache
                self.cache[cache_key] = result
                
                self.queue.push("asr_results", {**result, "trace_id": trace_id, "status": "completed"})
                logger.info("asr_complete", trace_id=trace_id)
                
            except Exception as e:
                logger.error("asr_failed", error=str(e), trace_id=trace_id)
                self.queue.push("asr_results", {"trace_id": trace_id, "status": "failed", "error": str(e)})

    async def run(self):
        logger.info("asr_worker_started", concurrency=settings.ASR_CONCURRENCY_LIMIT, gpu=settings.ASR_GPU_ENABLED)
        while True:
            try:
                # Read from asr job stream
                messages = self.queue.read_group(self.job_stream, self.group, self.consumer)
                for stream, msgs in messages:
                    for msg_id, data in msgs:
                        # Fire and forget / background task to allow concurrency
                        asyncio.create_task(self.process_job(msg_id, data))
                        self.queue.ack(stream, self.group, [msg_id])
                
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error("asr_worker_loop_error", error=str(e))
                await asyncio.sleep(1)

if __name__ == "__main__":
    worker = ASRWorker()
    asyncio.run(worker.run())
