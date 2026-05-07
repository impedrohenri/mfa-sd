import random

from app.core.redis_client import redis_client


def generate_code(email: str, prefix: str):

    code = str(random.randint(100000, 999999))

    redis_client.setex(
        f"{prefix}:{email}",
        300,
        code
    )

    return code


def verify_code(email: str, code: str, prefix: str):

    stored = redis_client.get(f"{prefix}:{email}")

    if not stored:
        return False

    if stored != code:
        return False

    redis_client.delete(f"{prefix}:{email}")

    return True