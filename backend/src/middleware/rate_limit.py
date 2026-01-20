from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.security import redis_client
import time
from src.schemas.errors import ERROR_RESPONSES

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip for health checks or static
        if request.url.path in ["/health", "/ready", "/metrics", "/docs", "/openapi.json"]:
             return await call_next(request)
             
        # Identify Client
        client_ip = request.client.host
        api_key = request.headers.get("X-API-Key")
        
        identifier = api_key if api_key else client_ip
        
        # Determine Limit
        limit = 100 # Default / Demo Tier
        if api_key:
            # Mock tier check
            if api_key.startswith("admin"):
                limit = 10000
            elif api_key.startswith("analyst"):
                limit = 1000
        
        # Redis Check
        if redis_client:
            key = f"rate_limit:{identifier}:{int(time.time() // 60)}"
            try:
                current = await redis_client.incr(key)
                if current == 1:
                    await redis_client.expire(key, 60)
                
                if current > limit:
                     return Response(
                         content='{"detail": "Rate limit exceeded"}', 
                         status_code=429, 
                         media_type="application/json"
                     )
            except Exception as e:
                # Fail open if Redis fails
                print(f"Rate limit error: {e}")
                pass
        
        response = await call_next(request)
        return response
