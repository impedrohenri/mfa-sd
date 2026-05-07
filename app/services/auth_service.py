import hashlib
import time

from app.utils.cryptography import (
    encrypt_email,
    decrypt_email
)

fake_users = {}


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def find_user_by_email(email: str):

    for encrypted_email, user_data in fake_users.items():

        decrypted_email = decrypt_email(encrypted_email)

        if decrypted_email == email:
            return encrypted_email, user_data

    return None, None


def create_user(email: str, password: str):

    existing_email, _ = find_user_by_email(email)

    if existing_email:
        return None

    encrypted_email = encrypt_email(email)

    fake_users[encrypted_email] = {
        "password": hash_password(password),
        "verified": False
    }

    return {
        "encrypted_email": encrypted_email,
        "password_hash": fake_users[encrypted_email]["password"]
    }


def verify_user(email: str):

    encrypted_email, user = find_user_by_email(email)

    if user:
        user["verified"] = True


def authenticate_user(email: str, password: str):

    encrypted_email, user = find_user_by_email(email)

    if not user:
        return False

    if not user["verified"]:
        return False

    return user["password"] == hash_password(password)


def generate_token():
    return f"fake-jwt-{int(time.time())}"