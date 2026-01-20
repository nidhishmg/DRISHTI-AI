from fastapi import FastAPI
from .api.webhook import router as webhook_router
from .core.monitoring import metrics_endpoint
from .core.logging import configure_logging

configure_logging()

app = FastAPI(title="Reality Gap AI - Ingestion Service")

# Include Webhooks
app.include_router(webhook_router)

# Health Checks
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    # In real app, check DB/Redis connectivity
    return {"status": "ready"}

# Metrics
@app.get("/metrics")
async def metrics():
    return metrics_endpoint(None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
