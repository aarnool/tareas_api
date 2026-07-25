from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from src.domains.users.schemas import UserResponse, UserCreate
from src.domains.users.dependencies import get_db
from sqlalchemy import select
from src.domains.users.models import User
from src.core.security import get_password_hash
from src.core.security import verify_password, DUMMY_HASH

router = APIRouter(
    prefix="/users",
    tags=["users"])

@router.post(
        "/register", 
        summary="Create a new user/Crear un nuevo usuario", 
        description="Create a new user with the provided information./Crear un nuevo usuario con la información proporcionada.",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED)
def register_user(
    user: Annotated[UserCreate, Body(description="The user information to create/La información del usuario a crear")],
    db: Annotated[Session, Depends(get_db)]):

    # Check if the user already exists
    stmt = select(User).where(User.username == user.username)
    user_exists = db.scalar(stmt)
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists/Usuario con este correo electrónico ya existe")

    stmt = select(User).where(User.email == user.email)
    email_exists = db.scalar(stmt)
    if email_exists:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered/Correo electrónico ya registrado")

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

