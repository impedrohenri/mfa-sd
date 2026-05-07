from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
import random
from app.middlewares.rate_limit import RateLimitMiddleware


from app.controllers import auth_controller

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

app.include_router(
    auth_controller.router,
    tags=["Auth"],
)

@app.get("/")
def root():
    return {"status": "ok"}
