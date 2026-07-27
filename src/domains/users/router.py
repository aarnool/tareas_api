from fastapi import APIRouter, Body, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from src.domains.users.schemas import UserResponse, UserCreate
from src.dependencies import get_db, get_current_user
from src.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
import src.domains.users.service as user_service

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

    return user_service.create_user(db, user)

@router.post(
        "/login",
        summary="Authenticate a user/Autenticar un usuario",
        description="Authenticate a user with the provided credentials./Autenticar un usuario con las credenciales proporcionadas.",
        status_code=status.HTTP_200_OK)

def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    response: Response):

    user = user_service.authenticate_user(db, form_data.username, form_data.password)

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

    return user_service.get_user_by_id(db, current_user["user_id"])


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("auth_token", path="/")
    return {"message": "Sesión cerrada"}