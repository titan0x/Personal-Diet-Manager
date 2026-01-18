import datetime
import hashlib
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def log_info(message: str):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[INFO {now}]: {message}")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)