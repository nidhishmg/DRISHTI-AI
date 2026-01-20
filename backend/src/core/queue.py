from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json
import os
import redis
from tenacity import retry, stop_after_attempt, wait_exponential
from .logging import logger
from .tracing import get_trace_id

class QueueInterface(ABC):
    @abstractmethod
    def push(self, stream: str, payload: Dict[str, Any]) -> str:
        pass
        
    @abstractmethod
    def read_group(self, stream: str, group: str, consumer: str, count: int = 1) -> list:
        pass

    @abstractmethod
    def ack(self, stream: str, group: str, message_ids: list):
        pass

class RedisQueue(QueueInterface):
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        logger.info("connected_to_redis", url=self.redis_url)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def push(self, stream: str, payload: Dict[str, Any]) -> str:
        """Push a message to a Redis Stream with trace ID auto-injection."""
        if "trace_id" not in payload:
            payload["trace_id"] = get_trace_id()
            
        # Redis streams store keys/values as strings. Serialize JSON if needed or store flat.
        # Here we store flat string items. Complex nested objects should be JSON dumped.
        flat_payload = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) 
                        for k, v in payload.items()}
        
        msg_id = self.client.xadd(stream, flat_payload)
        logger.info("queue_push", stream=stream, msg_id=msg_id, trace_id=payload["trace_id"])
        return msg_id

    def read_group(self, stream: str, group: str, consumer: str, count: int = 1) -> list:
        try:
            # Create group if not exists
            try:
                self.client.xgroup_create(stream, group, mkstream=True)
            except redis.exceptions.ResponseError as e:
                if "BUSYGROUP" not in str(e):
                    raise
            
            # Read new messages
            messages = self.client.xreadgroup(group, consumer, {stream: ">"}, count=count)
            return messages
        except Exception as e:
            logger.error("queue_read_error", error=str(e), stream=stream)
            return []

    def ack(self, stream: str, group: str, message_ids: list):
        if message_ids:
            self.client.xack(stream, group, *message_ids)
