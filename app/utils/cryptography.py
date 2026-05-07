import os

from cryptography.fernet import Fernet

SECRET_KEY = os.getenv("SECRET_KEY")

cipher = Fernet(SECRET_KEY)


def encrypt_email(email: str) -> str:
    return cipher.encrypt(email.encode()).decode()


def decrypt_email(email: str) -> str:
    return cipher.decrypt(email.encode()).decode()