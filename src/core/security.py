"""Módulo con utilidades criptográficas y gestión de tokens JWT."""
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt
from src.config import settings

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")   

def get_password_hash(password: str) -> str:
    """Genera el hash seguro de una contraseña en texto plano."""
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con su versión cifrada."""
    return password_hash.verify(plain_password, hashed_password)

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea y firma un token JWT con tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt