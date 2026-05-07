from fastapi import Request
from fastapi.responses import JSONResponse
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

            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Try again later."
                }
            )

        pipe = redis_client.pipeline()

        pipe.incr(key, 1)
        pipe.expire(key, WINDOW_SECONDS)

        pipe.execute()

        response = await call_next(request)

        return response