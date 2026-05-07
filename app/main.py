from fastapi import FastAPI
import redis
import os
import random
from app.middlewares.rate_limit import RateLimitMiddleware


from app.controllers.auth_controller import auth_controller

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

app.include_router(
    auth_controller.router,
    prefix="/auth",
    tags=["Auth"],
)

@app.get("/")
def root():
    return {"status": "ok"}
