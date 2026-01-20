from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# Metrics
COMPLAINT_COUNTER = Counter(
    "complaints_ingested_total", 
    "Total number of complaints ingested", 
    ["ids", "source"]
)

PROCESSING_LATENCY = Histogram(
    "processing_latency_seconds", 
    "Time taken to process a complaint chunk", 
    ["stage"]
)

QUEUE_DEPTH = Gauge( "queue_depth_count", "Current depth of ingestion queue", ["queue_name"]) if 'Gauge' in globals() else None
# Note: prometheus_client Gauge must be imported. 
from prometheus_client import Gauge
QUEUE_DEPTH = Gauge("queue_depth_count", "Current depth of ingestion queue", ["queue_name"])

DEDUP_HIT_RATE = Counter("dedup_hit_total", "Total duplicate content detected", ["method"])

def metrics_endpoint(request):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
