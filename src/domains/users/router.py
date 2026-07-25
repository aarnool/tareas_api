from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from typing import Annotated
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.domains.users.schemas import UserResponse, UserCreate, UserUpdate
from src.domains.users.dependencies import get_db
from sqlalchemy import select
from src.domains.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"])

@router.post(
        "", 
        summary="Create a new user/Crear un nuevo usuario", 
        description="Create a new user with the provided information./Crear un nuevo usuario con la información proporcionada.",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED)
def create_user(
    user: Annotated[UserCreate, Body(description="The user information to create/La información del usuario a crear")],
    db: Annotated[Session, Depends(get_db)]):

    # Check if the user already exists
    stmt = select(User).where(User.email == user.email)
    user_exists = db.scalar(stmt)
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists/Usuario con este correo electrónico ya existe")

    # Create a new user instance
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", 
        summary="Get user by ID/Obtener usuario por ID",
        description="Retrieve a user by their unique ID./Recuperar un usuario por su ID único.",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: Annotated[int, Path(description="The ID of the user to retrieve/El Id del usuario a recuperar")],
    db: Annotated[Session, Depends(get_db)]):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail="User not found/Usuario no encontrado")
    return user

@router.get("",
        summary="Get all users/Obtener todos los usuarios",
        description="Retrieve a list of all users./Recuperar una lista de todos los usuarios./Recuperar una lista de todos los usuarios.",
        response_model=list[UserResponse],
        status_code=status.HTTP_200_OK)
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    start: Annotated[
        int, Query(
            description="The starting index for retrieving users/El índice de inicio para recuperar usuarios")] = 0,
    limit: Annotated[
        int, Query(
            description="The maximum number of users to retrieve/El número máximo de usuarios a recuperar")]= 10):
    users = db.execute(select(User).offset(start).limit(limit)).scalars().all()
    return users

@router.patch("/{user_id}",
        summary="Update user by ID/Actualizar usuario por ID",
        description="Update a user's information by their unique ID./Actualizar la información de un usuario por su ID único.",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK)
def update_user(
    user_id: Annotated[int, Path(description="The ID of the user to update/El Id del usuario a actualizar")],
    user_update: Annotated[UserUpdate, Body(description="The updated user information/La información actualizada del usuario")],
    db: Annotated[Session, Depends(get_db)]):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found/Usuario no encontrado")
    
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}",
        summary="Delete user by ID/Eliminar usuario por ID",
        description="Delete a user by their unique ID./Eliminar un usuario por su ID único.",
        status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: Annotated[int, Path(description="The ID of the user to delete/El Id del usuario a eliminar")],
    db: Annotated[Session, Depends(get_db)]):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail="User not found/Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully/Usuario eliminado con éxito"}
