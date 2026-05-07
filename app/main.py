from fastapi import FastAPI
import redis
import os
import random

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/generate-code/{user_id}")
def generate_code(user_id: str):
    code = str(random.randint(100000, 999999))
    redis_client.setex(f"mfa:{user_id}", 900, code)  # expira em 5 min
    return {"code": code}

@app.post("/verify-code/{user_id}/{code}")
def verify_code(user_id: str, code: str):
    stored = redis_client.get(f"mfa:{user_id}")
    
    if stored == code:
        redis_client.delete(f"mfa:{user_id}")
        return {"valid": True}
    
    return {"valid": False}