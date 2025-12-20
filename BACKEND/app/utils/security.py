import hashlib
import secrets
from datetime import datetime, timedelta
from jose import jwt
from app.utils.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# ===== CONFIG =====
SECRET_KEY = "SUPER_SECRET_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ===== PASSWORD UTILS =====
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain: str, hashed: str) -> bool:
    salt, hash_val = hashed.split("$")
    return hashlib.sha256((salt + plain).encode()).hexdigest() == hash_val


# ===== JWT =====
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
