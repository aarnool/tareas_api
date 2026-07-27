from src.database import SessionLocal
from fastapi import Cookie
from typing import Annotated
import jwt
from src.core.security import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(auth_token: Annotated[str | None, Cookie()] = None) -> dict:
    if auth_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated/No autenticado"
        )
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired/El token ha expirado",
    
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token/Token inválido",
        )   
        
    
