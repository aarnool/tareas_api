"""Módulo de esquemas Pydantic para la validación y serialización de usuarios."""
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Esquema base con los atributos comunes de usuario."""
    username: str = Field(
        description="The full name or username of the user / El nombre de usuario o nombre completo",
        examples=["johndoe"]
    )
    email: EmailStr = Field(
        description="The email address of the user / El correo electrónico del usuario",
        examples=["john.doe@example.com"]
    )


class UserCreate(UserBase):
    """Esquema para la petición de registro de un usuario."""
    password: str = Field(
        description="The plain text password of the user / La contraseña en texto plano del usuario",
        examples=["secretPassword123!"]
    )


class UserUpdate(BaseModel):
    """Esquema para la actualización de datos de un usuario."""
    username: str | None = Field(
        default=None,
        description="The full name or username of the user / El nombre de usuario o nombre completo",
        examples=["johndoe_updated"]
    )
    email: EmailStr | None = Field(
        default=None,
        description="The email address of the user / El correo electrónico del usuario",
        examples=["john.updated@example.com"]
    )


class UserResponse(UserBase):
    """Esquema de respuesta devuelto al cliente."""
    id: int = Field(
        description="The unique identifier of the user in the database / El identificador único del usuario",
        examples=[1]
    )

    model_config = {
        "from_attributes": True
    }


class MessageResponse(BaseModel):
    """Esquema para mensajes de respuesta informativos."""
    message: str = Field(
        description="Informative message about the operation result / Mensaje informativo del resultado de la operación",
        examples=["Login successful/Inicio de sesión exitoso"]
    )