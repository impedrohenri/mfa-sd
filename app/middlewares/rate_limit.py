from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import redis_client

MAX_REQUESTS = 20
WINDOW_SECONDS = 10

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host

        key = f"rate_limit:{ip}"

        current = redis_client.get(key)

        if current and int(current) >= MAX_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

        pipe = redis_client.pipeline()

        pipe.incr(key, 1)
        pipe.expire(key, WINDOW_SECONDS)

        pipe.execute()

        response = await call_next(request)

        return response