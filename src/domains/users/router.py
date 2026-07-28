"""Módulo enrutador con endpoints para gestión y autenticación de usuarios."""
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.domains.users.schemas import MessageResponse, UserCreate, UserResponse
import src.domains.users.service as user_service


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error / Error interno del servidor"
        }
    }
)


@router.post(
    "/register",
    summary="Create a new user / Crear un nuevo usuario",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="User successfully registered / Usuario registrado exitosamente",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request - Email or username already taken / Correo o usuario ya registrados",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email and username already registered/Correo electonico y nombre de usuario ya registrados"
                    }
                }
            }
        }
    }
)
def register_user(
    user: Annotated[
        UserCreate,
        Body(description="The user information to create / La información del usuario a crear")
    ],
    db: Annotated[Session, Depends(get_db)]
):
    """
    **Register a new user account / Registrar una nueva cuenta de usuario**

    Creates a new user in the database with the provided credentials.
    Crea un nuevo usuario en la base de datos con las credenciales proporcionadas.

    ### Validations / Validaciones:
    - **username**: Must be unique in the system / Debe ser único en el sistema.
    - **email**: Must have a valid format and be unique / Debe tener un formato válido y ser único.
    - **password**: Securely hashed before storing / Se cifra de manera segura antes de almacenarse.
    """
    return user_service.create_user(db, user)


@router.post(
    "/login",
    summary="Authenticate a user / Autenticar un usuario",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    response_description="Login confirmation message and HTTP-only cookie / Confirmación y cookie de sesión",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request - Incorrect email or password / Correo o contraseña incorrecta",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incrorrect email or passwoard/Correo o Contraseña incorrecta"
                    }
                }
            }
        }
    }
)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    response: Response
):
    """
    **User Authentication / Autenticación de usuario**

    Authenticates a user using OAuth2 compatible form data and sets a secure JWT cookie.
    Autentica al usuario mediante formulario OAuth2 y genera una cookie segura JWT.

    ### Details / Detalles:
    - **username**: Enter the registered **email** address / Ingresa el **correo electrónico** registrado.
    - **password**: Enter the user's password / Ingresa la contraseña del usuario.
    - **Cookie**: On success, an HTTP-only cookie named `auth_token` is set in the client browser / Al tener éxito, se configura una cookie HTTP-only llamada `auth_token`.
    """
    return user_service.login_user(db, form_data, response)


@router.get(
    "/me",
    summary="Get current user information / Obtener información del usuario actual",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    response_description="Authenticated user profile data / Datos del usuario autenticado",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing, invalid, or expired session cookie / No autenticado o token inválido",
            "content": {
                "application/json": {
                    "examples": {
                        "missing_cookie": {
                            "summary": "Cookie missing / Cookie faltante",
                            "value": {"detail": "Not authenticated/No autenticado"}
                        },
                        "expired_token": {
                            "summary": "Token expired / Token expirado",
                            "value": {"detail": "Token has expired/El token ha expirado"}
                        },
                        "invalid_token": {
                            "summary": "Token invalid / Token inválido",
                            "value": {"detail": "Invalid token/Token inválido"}
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found - User record not found in database / Usuario no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found/Usuario no encontrado"
                    }
                }
            }
        }
    }
)
def get_current_user_info(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    **Retrieve Current User Profile / Recuperar perfil del usuario autenticado**

    Returns the profile information of the user making the request.
    Devuelve la información de perfil del usuario que realiza la petición.

    ### Security / Seguridad:
    Requires a valid `auth_token` cookie in the request headers / Requiere una cookie `auth_token` válida en las cabeceras.
    """
    return user_service.get_user_by_id(db, current_user["user_id"])


@router.post(
    "/logout",
    summary="Log out user / Cerrar sesión del usuario",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    response_description="Logout confirmation message / Mensaje de confirmación de cierre de sesión",
    responses={
        status.HTTP_200_OK: {
            "description": "Session closed successfully / Sesión cerrada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Sesión cerrada"
                    }
                }
            }
        }
    }
)
def logout(response: Response):
    """
    **User Logout / Cierre de sesión de usuario**

    Terminates the current user session by deleting the authentication cookie from the client browser.
    Termina la sesión actual del usuario eliminando la cookie de autenticación del navegador cliente.

    ### Details / Detalles:
    - Instructs the browser to remove the `auth_token` cookie by setting its expiration in the past / Instruye al navegador para eliminar la cookie `auth_token`.
    """
    response.delete_cookie(
        "auth_token", 
        path="/",
        secure=True,
        httponly=True,
        samesite="none")
    return {"message": "Sesión cerrada"}