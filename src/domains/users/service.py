"""Módulo de lógica de negocio y operaciones de base de datos para usuarios."""
from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from src.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, DUMMY_HASH, create_access_token, get_password_hash, verify_password
from src.domains.users.models import User
from src.domains.users.schemas import UserCreate
import src.domains.users.service as user_service


def create_user(db: Session, user: UserCreate) -> User:
    """Crea un nuevo usuario validando que el correo y usuario no estén registrados."""
    # Verificar si el usuario ya existe
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

    new_user = User(
        username=user.username,
        email=user.email,
        password=password_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, form_data: OAuth2PasswordRequestForm, response: Response):
    """Inicia sesión de un usuario verificando sus credenciales."""
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    
    auth_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )

    response.set_cookie(
        key="auth_token",
        value=auth_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {
        "message": "Login successful/Inicio de sesión exitoso"
    }


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Autentica un usuario verificando sus credenciales y protegiendo contra ataques de temporización."""
    stmt = select(User).where(or_(User.email == email, User.username == email))
    user = db.scalar(stmt)
    if not user:
        verify_password(password, DUMMY_HASH)  # Evitar ataques de temporización
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
    """Obtiene un usuario por su identificador único."""
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found/Usuario no encontrado"
        )
    
    return user

