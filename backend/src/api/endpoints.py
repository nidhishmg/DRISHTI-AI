from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
# Phase 3 Endpoints
from typing import List, Dict, Any, Union

from datetime import datetime, timedelta
import random
from uuid import uuid4

from .schemas.models import Cluster, FailureArchetype, Intervention
from .schemas.errors import ErrorResponse, BadRequestError, UnauthorizedError, RateLimitExceededError, InternalServerError
from .core.security import (
    create_access_token, create_refresh_token, Token, User, 
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS,
    revoke_token, require_role, oauth2_scheme
)
from .middleware.rate_limit import RateLimitMiddleware
from .core.export import SecureExportManager
from fastapi import Response, Request



ERROR_RESPONSES = {
    400: {"model": BadRequestError, "description": "Bad Request"},
    401: {"model": UnauthorizedError, "description": "Unauthorized"},
    429: {"model": RateLimitExceededError, "description": "Too Many Requests"},
    500: {"model": InternalServerError, "description": "Internal Server Error"},
}


router = APIRouter()

# --- Auth Endpoints (for Demo) ---
@router.post("/token", response_model=Token, tags=["auth"], responses=ERROR_RESPONSES)
async def login_for_access_token(response: Response, form_data: User): # Simplified login
    # In a real app, verify password. Here, just issue token for the role.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": form_data.username, "role": form_data.role},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": form_data.username, "role": form_data.role},
        expires_delta=refresh_token_expires
    )
    
    # Set Secure Cookie for Refresh Token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, # Ensure HTTPS
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token, tags=["auth"], responses=ERROR_RESPONSES)
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    # Verify (logic simplified, ideally verify signature + expiration)
    # Re-issue both
    # For Hackathon: assuming valid if present and trusted
    # Real logic: decode, check exp, check type='refresh'
    
    # Mock regeneration
    new_access_token = create_access_token(data={"sub": "refreshed_user", "role": "analyst"})
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token, # Keep same or rotate
        "token_type": "bearer"
    }

@router.post("/logout", tags=["auth"], responses=ERROR_RESPONSES)
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    await revoke_token(token, 3600) # Revoke for 1 hr
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


# --- Ingestion Endpoints ---
@router.post("/ingest/voice", tags=["ingestion"], responses=ERROR_RESPONSES)
async def ingest_voice(file: UploadFile = File(...)):
    """
    Mock voice ingestion.
    In real flow: Save file -> Whisper -> Text -> Process.
    """
    # Validation
    MAX_SIZE = 10 * 1024 * 1024 # 10MB
    ALLOWED_TYPES = ["audio/mpeg", "audio/wav", "audio/x-m4a"]
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: mp3, wav, m4a")
        
    # Check size (mock check as we don't want to read whole file into memory if huge, but for demo we can check header/size)
    # real check happens during read chunking
    if file.size and file.size > MAX_SIZE:
         raise HTTPException(status_code=400, detail="File too large (Max 10MB)")

    # Simulate processing delay or ID generation

    trace_id = str(uuid4())
    return {
        "status": "queued",
        "trace_id": trace_id,
        "filename": file.filename,
        "message": "Voice uploaded and queued for transcription."
    }

# --- Intelligence / Visualization Endpoints ---

@router.get("/dashboard/stats", tags=["metrics"], responses=ERROR_RESPONSES)
async def get_dashboard_stats():
    """
    Return aggregated stats for the dashboard.
    """
    return {
        "total_reports": 12345,
        "reports_trend": 18.2,
        "active_clusters": 42,
        "critical_clusters": 5,
        "avg_trust_score": 0.924,
        "causal_confidence": 0.87
    }



@router.get("/clusters/hot", response_model=List[Cluster], tags=["clustering"], responses=ERROR_RESPONSES)
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

@router.get("/graph/archetypes", response_model=Dict[str, Any], tags=["causal"], responses=ERROR_RESPONSES)
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

@router.post("/intervention/simulate", response_model=Intervention, tags=["interventions"], responses=ERROR_RESPONSES, dependencies=[Depends(require_role(["admin", "analyst"]))])


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

@router.get("/export/complaint/{complaint_id}", tags=["export"], responses=ERROR_RESPONSES)
async def export_complaint(complaint_id: str, current_user: int = Depends(require_role(["admin", "analyst"]))):
    """
    Securely export complaint data with chain of custody and watermark.
    """
    manager = SecureExportManager()
    
    # Mock data fetch
    data = {"id": complaint_id, "text": "Sample complaint data...", "status": "resolved"}
    
    encrypted_package = manager.create_encrypted_package(data, "demo_pass")
    
    return Response(
        content=encrypted_package,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=complaint_{complaint_id}.pdf"}
    )

