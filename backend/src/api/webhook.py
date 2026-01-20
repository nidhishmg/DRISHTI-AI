from fastapi import APIRouter, Request, HTTPException, Depends
from ..schemas.models import Complaint, SourceType
from ..core.queue import RedisQueue
from ..core.security import hash_phone_number, strip_pii
from ..core.tracing import generate_trace_id
from ..core.logging import logger
from datetime import datetime

router = APIRouter()
queue = RedisQueue()

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    # Basic rate limiting (IP based) should be handled by middleware or load balancer (e.g. nginx/traefik)
    # or using a library like slowapi. For now, assuming standard setup.
    
    payload = await request.json()
    trace_id = generate_trace_id()
    
    logger.info("whatsapp_received", trace_id=trace_id)

    # Simplified extraction logic based on theoretical WhatsApp Business API payload
    try:
        # Extract message
        # This structure is hypothetical for the example
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
             return {"status": "ok"} # Ack heartbeat

        msg = messages[0]
        from_number = msg.get("from") # PII
        text_body = msg.get("text", {}).get("body", "")
        
        # PII Handling
        hashed_phone = hash_phone_number(from_number)
        clean_text = strip_pii(text_body)
        
        complaint = Complaint(
            trace_id=trace_id,
            source=SourceType.WHATSAPP,
            raw_text=clean_text,
            location=None, # Extract specific location if available
            entities={"sender_hash": hashed_phone} # Store hashed ID
        )
        
        # Push to data stream
        queue.push("complaint_events", complaint.model_dump(mode='json'))
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error("whatsapp_error", error=str(e), trace_id=trace_id)
        raise HTTPException(status_code=500, detail="Processing failed")
