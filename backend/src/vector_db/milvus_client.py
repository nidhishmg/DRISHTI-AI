import logging
import time
from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType
from src.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class MilvusClient:
    def __init__(self):
        self.host = "milvus" # internal docker dns
        self.port = "19530"
        self.collection_name = "complaint_vectors"
        self.connected = False

    def connect(self):
        try:
            connections.connect("default", host=self.host, port=self.port)
            self.connected = True
            logger.info("Connected to Milvus")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            self.connected = False

    def health_check(self) -> bool:
        if not self.connected:
            self.connect()
        try:
            return utility.has_collection(self.collection_name)
        except Exception:
            return False

    def optimize_index(self):
        """Periodic job to compact and reindex."""
        if not self.health_check():
            return
            
        logger.info("Starting Milvus optimization...")
        try:
             c = Collection(self.collection_name)
             c.compact()
             logger.info("Milvus compaction completed.")
             
             # Re-index if needed (simple logic: just create if missing, or force re-build if drift high)
             # Here we verify index existence
             if not c.has_index():
                 index_params = {
                     "metric_type": "L2",
                     "index_type": "IVF_FLAT",
                     "params": {"nlist": 1024}
                 }
                 c.create_index(field_name="embedding", index_params=index_params)
                 logger.info("Milvus index (re)created.")
        except Exception as e:
             logger.error(f"Milvus optimization failed: {e}")

    def prune_old_data(self, retention_days: int = 90):
        """TTL Policy Enforcer."""
        if not self.health_check():
            return
        
        # Calculate timestamp threshold (mock logic as Milvus deletions by expr are specific)
        # expr = f"timestamp < {threshold}"
        # c.delete(expr)
        pass 
