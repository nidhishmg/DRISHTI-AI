-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum types (mapped to text for compatibility/simplicity or strict enums)
CREATE TYPE source_type AS ENUM ('youtube', 'twitter', 'app_review', 'whatsapp', 'news');

-- Complaint Table
CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trace_id TEXT NOT NULL,
    source source_type NOT NULL,
    raw_text TEXT NOT NULL,
    transcript_metadata JSONB,
    location JSONB,
    detected_scheme TEXT[],
    entities JSONB,
    embedding_id TEXT,
    quality_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Hardening
    hash_fingerprint TEXT,
    dedup_confidence FLOAT
);

-- Cluster Table
CREATE TABLE IF NOT EXISTS clusters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    summary TEXT,
    trend_metrics JSONB,
    geo_distribution JSONB,
    linked_scheme_ids TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Hardening
    confidence_score FLOAT,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- FailureArchetype Table
CREATE TABLE IF NOT EXISTS failure_archetypes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    causal_graph_ref TEXT,
    confidence_score FLOAT
);

-- Intervention Table
CREATE TABLE IF NOT EXISTS interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    cost_estimate FLOAT,
    expected_impact INTEGER,
    confidence FLOAT
);

-- DataLineage Table
CREATE TABLE IF NOT EXISTS data_lineage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID REFERENCES complaints(id),
    source_module TEXT NOT NULL,
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_stage TEXT NOT NULL,
    checksum TEXT NOT NULL,
    version INTEGER NOT NULL
);

-- ContentFingerprint Table
CREATE TABLE IF NOT EXISTS content_fingerprints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID REFERENCES complaints(id),
    simhash TEXT NOT NULL,
    minhash_signature JSONB NOT NULL, -- Storing List[int] as JSONB
    source TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UserConsent Table
CREATE TABLE IF NOT EXISTS user_consents (
    phone_hash TEXT PRIMARY KEY,
    consent_version TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    channel TEXT NOT NULL
);

-- TraceLog Table
CREATE TABLE IF NOT EXISTS trace_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trace_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT NOT NULL,
    message TEXT,
    metadata JSONB
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_complaints_source ON complaints(source);
CREATE INDEX IF NOT EXISTS idx_complaints_trace_id ON complaints(trace_id);
CREATE INDEX IF NOT EXISTS idx_complaints_hash_fingerprint ON complaints(hash_fingerprint);
CREATE INDEX IF NOT EXISTS idx_trace_logs_trace_id ON trace_logs(trace_id);
CREATE INDEX IF NOT EXISTS idx_user_consents_phone_hash ON user_consents(phone_hash);
