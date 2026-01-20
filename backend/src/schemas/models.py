from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, HttpUrl, field_validator
import re
from enum import Enum


class SourceType(str, Enum):
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    APP_REVIEW = "app_review"
    WHATSAPP = "whatsapp"
    NEWS = "news"

class ProcessingStage(str, Enum):
    INGEST = "ingest"
    QUEUE = "queue"
    PERSIST = "persist"
    DEDUP = "dedup"
    PII_STRIP = "pii_strip"

class TraceStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"

class TraceLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    trace_id: str
    stage: ProcessingStage
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: TraceStatus
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class Complaint(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    trace_id: str
    source: SourceType
    raw_text: str
    transcript_metadata: Optional[Dict[str, Any]] = None  # duration, path
    location: Optional[Dict[str, Any]] = None  # lat, lon, state, district
    detected_scheme: List[str] = Field(default_factory=list)
    entities: Optional[Dict[str, Any]] = None
    embedding_id: Optional[str] = None
    quality_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Hardening fields
    hash_fingerprint: Optional[str] = None
    dedup_confidence: Optional[float] = None
    
    @field_validator('raw_text')
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        # Basic sanitization: remove HTML tags, limit length
        clean = re.sub(r'<[^>]*>', '', v)
        if len(clean) > 5000:
            raise ValueError("Text too long")
        return clean


class Cluster(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    summary: str
    trend_metrics: Dict[str, Any]  # count_30d, growth_rate
    geo_distribution: Dict[str, Any]
    linked_scheme_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Hardening fields
    confidence_score: Optional[float] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class FailureArchetype(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    causal_graph_ref: Optional[str] = None
    confidence_score: Optional[float] = None

class Intervention(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    cost_estimate: Optional[float] = None
    expected_impact: Optional[int] = None
    confidence: Optional[float] = None

class DataLineage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    complaint_id: UUID
    source_module: str
    ingestion_timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_stage: str
    checksum: str
    version: int

class ContentFingerprint(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    complaint_id: UUID
    simhash: str
    minhash_signature: List[int]
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserConsent(BaseModel):
    phone_hash: str  # SHA-256 + salt
    consent_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    channel: str
