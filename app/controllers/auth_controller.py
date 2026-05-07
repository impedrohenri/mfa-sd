from fastapi import APIRouter, Depends, status, Header
from app.core.redis_client import redis_client
import random

router = APIRouter()

@router.post("/generate-code/{user_id}")
def generate_code(user_id: str):
    code = str(random.randint(100000, 999999))
    redis_client.setex(f"mfa:{user_id}", 900, code)  # expira em 5 min
    return {"code": code}

@router.post("/verify-code/{user_id}/{code}")
def verify_code(user_id: str, code: str):
    stored = redis_client.get(f"mfa:{user_id}")
    
    if stored == code:
        redis_client.delete(f"mfa:{user_id}")
        return {"valid": True}
    
    return {"valid": False}