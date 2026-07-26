from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.core.security import DUMMY_HASH, get_password_hash, verify_password
from src.domains.users.models import User
from src.domains.users.schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    # Check if the user already exists
    stmt = select(User).where(User.username == user.username)
    user_exists = db.scalar(stmt)
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="Email and username already registered/Correo electonico y nombre de usuario ya registrados"
        )

    stmt = select(User).where(User.email == user.email)
    email_exists = db.scalar(stmt)
    if email_exists:
        raise HTTPException(
            status_code=400, 
            detail="Email and username already registered/Correo electonico y nombre de usuario ya registrados"
        )

    password_hash = get_password_hash(user.password)

    # Create a new user instance
    new_user = User(
        username=user.username,
        email=user.email,
        password=password_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User:
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)
    if not user:
        verify_password(password, DUMMY_HASH)  # Prevent timing attacks
        raise HTTPException(
            status_code=400, 
            detail="Incrorrect email or passwoard/Correo o Contraseña incorrecta"
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=400, 
            detail="Incrorrect email or passwoard/Correo o Contraseña incorrecta"
        )

    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found/Usuario no encontrado"
        )
    
    return user
