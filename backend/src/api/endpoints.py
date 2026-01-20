from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
# Phase 3 Endpoints
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from uuid import uuid4

from .schemas.models import Cluster, FailureArchetype, Intervention
from .core.security import create_access_token, Token, User, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# --- Auth Endpoints (for Demo) ---
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: User): # Simplified login
    # In a real app, verify password. Here, just issue token for the role.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": form_data.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Ingestion Endpoints ---
@router.post("/ingest/voice")
async def ingest_voice(file: UploadFile = File(...)):
    """
    Mock voice ingestion.
    In real flow: Save file -> Whisper -> Text -> Process.
    """
    # Simulate processing delay or ID generation
    trace_id = str(uuid4())
    return {
        "status": "queued",
        "trace_id": trace_id,
        "filename": file.filename,
        "message": "Voice uploaded and queued for transcription."
    }

# --- Intelligence / Visualization Endpoints ---

@router.get("/clusters/hot", response_model=List[Cluster])
async def get_hot_clusters():
    """
    Return top 'hot' clusters for the dashboard.
    Mocking data to ensure UI has something to render.
    """
    # Mock data
    return [
        Cluster(
            title="Pension Scheme Delays - Karnataka",
            summary="Multiple reports of 3+ month delays provided by elderly citizens in rural districts.",
            trend_metrics={"count_30d": 142, "growth_rate": 15.5},
            geo_distribution={"Karnataka": 80, "Rural": 60, "Urban": 20},
            confidence_score=0.92
        ),
        Cluster(
            title="Ration Card Biometric Failures",
            summary="Fingerprint scanners failing intermittently in North Zones, causing denial of service.",
            trend_metrics={"count_30d": 89, "growth_rate": 8.2},
            geo_distribution={"North Zone": 75, "Bihar": 25},
            confidence_score=0.88
        ),
        Cluster(
            title="Mid-day Meal Quality Issues",
            summary="Reports of sub-standard quality grain being supplied in primary schools.",
            trend_metrics={"count_30d": 56, "growth_rate": -2.1},
            geo_distribution={"Odisha": 90},
            confidence_score=0.75
        )
    ]

@router.get("/graph/archetypes", response_model=Dict[str, Any])
async def get_causal_graph():
    """
    Return node-edge structure for the Causal Graph visualization.
    """
    return {
        "nodes": [
            {"id": 1, "label": "Biometric Failure", "group": "failure"},
            {"id": 2, "label": "Network Outage", "group": "root_cause"},
            {"id": 3, "label": "Pension Denial", "group": "outcome"},
            {"id": 4, "label": "Staff Training", "group": "intervention"},
        ],
        "edges": [
            {"from": 2, "to": 1, "label": "causes", "arrows": "to"},
            {"from": 1, "to": 3, "label": "leads_to", "arrows": "to"},
            {"from": 4, "to": 1, "label": "mitigates", "arrows": "to", "dashes": True}
        ]
    }

@router.post("/intervention/simulate", response_model=Intervention)
async def simulate_intervention(cluster_id: str, intensity: float = 0.5):
    """
    Simulate the effect of a policy change.
    """
    return Intervention(
        title="Automated Offline-Auth Fallback",
        cost_estimate=intensity * 50000, # Mock logic
        expected_impact=int(intensity * 100), # Mock logic: lives impacted
        confidence=0.85
    )
