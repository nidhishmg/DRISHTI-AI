from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.webhook import router as webhook_router
from .api.endpoints import router as api_router
from .core.monitoring import metrics_endpoint
from .core.logging import configure_logging
from .middleware.rate_limit import RateLimitMiddleware


configure_logging()

app = FastAPI(title="Reality Gap AI - Ingestion Service")

# CORS Middleware (Enable for Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)


# Include Webhooks & API
app.include_router(webhook_router, prefix="/webhook", tags=["webhooks"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])
# Health Checks
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    # In real app, check DB/Redis connectivity
    return {"status": "ready"}

# Metrics
@app.get("/metrics", tags=["metrics"])
async def metrics():
    return metrics_endpoint(None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
