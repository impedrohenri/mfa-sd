import hashlib
import time

fake_users = {}


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(email: str, password: str):

    if email in fake_users:
        return None

    fake_users[email] = {
        "password": hash_password(password),
        "verified": False
    }

    return fake_users[email]


def verify_user(email: str):
    if email in fake_users:
        fake_users[email]["verified"] = True


def authenticate_user(email: str, password: str):

    user = fake_users.get(email)

    if not user:
        return False

    if not user["verified"]:
        return False

    return user["password"] == hash_password(password)


def generate_token():
    return f"fake-jwt-{int(time.time())}"