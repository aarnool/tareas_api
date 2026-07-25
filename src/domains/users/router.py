from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from src.domains.users.schemas import UserResponse, UserCreate
from src.domains.users.dependencies import get_db, get_current_user
from sqlalchemy import select
from src.domains.users.models import User
from src.core.security import get_password_hash
from src.core.security import verify_password, DUMMY_HASH, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

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

@router.post(
        "/login",
        summary="Authenticate a user/Autenticar un usuario",
        description="Authenticate a user with the provided credentials./Autenticar un usuario con las credenciales proporcionadas.",
        status_code=status.HTTP_200_OK)

def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    response: Response):

    stmt = select(User).where(User.email == form_data.username)
    user = db.scalar(stmt)
    if not user:
        verify_password(form_data.password, DUMMY_HASH)  # Prevent timing attacks
        raise HTTPException(
            status_code=400, 
            detail="Incrorrect email or passwoard/Correo o Contraseña incorrecta")
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, 
            detail="Incrorrect email or passwoard/Correo o Contraseña incorrecta")

    auth_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )

    response.set_cookie(
        key="auth_token",
        value=auth_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age= ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {
        "message": "Login successful/Inicio de sesión exitoso"
    }

@router.get(
        "/me",
        summary="Get current user information/Obtener información del usuario actual",
        description="Retrieve the information of the authenticated user./Recuperar la información del usuario autenticado.",
        response_model=UserResponse,)

def get_current_user_info(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]):

    stmt = select(User).where(User.id == current_user["user_id"])
    user = db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found/Usuario no encontrado"
        )
    
    return user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("auth_token", path="/")
    return {"message": "Sesión cerrada"}