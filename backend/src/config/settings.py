import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Reality Gap AI"
    ENV: str = "development"
    DEBUG: bool = True
    
    # Paths
    MODEL_CACHE_DIR: str = "/models"
    
    # Model Configuration (Patch A - Hot Swapping)
    WHISPER_MODEL: str = "faster-whisper-medium"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    NER_MODEL: str = "xx_ent_wiki_sm"
    
    # Feature Flags
    ENABLE_STREAM_PROCESSING: bool = True
    
    # ML Pipeline Constraints
    MAX_AUDIO_DURATION_SEC: int = 300
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    DRIFT_THRESHOLD: float = 0.15

    # API Keys
    OPENAI_API_KEY: str = ""
    
    # Patch 7: Clustering Optimization
    FULL_RECLUSTER: bool = False
    LSH_ENABLED: bool = True
    CLUSTERING_BATCH_SIZE: int = 1000
    
    # Patch 8: ASR Scaling
    ASR_WORKER_POOL_SIZE: int = 2
    ASR_GPU_ENABLED: bool = False
    ASR_CONCURRENCY_LIMIT: int = 5



    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
