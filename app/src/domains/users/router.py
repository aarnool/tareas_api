from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.src.database import SessionLocal
from app.src.domains.users.schemas import UserResponse, UserCreate
from app.src.domains.users.dependencies import get_db
from sqlalchemy import select
from app.src.domains.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"])

@router.post(
        "", 
        summary="Create a new user", 
        description="Create a new user with the provided information.",
        response_model=UserResponse)
def create_user(
    user: Annotated[UserCreate, Body(description="The user information to create")],
    db: Annotated[Session, Depends(get_db)]):

    # Check if the user already exists
    stmt = select(User).where(User.email == user.email)
    user_exists = db.scalar(stmt)
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists")

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