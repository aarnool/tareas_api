"""Módulo de modelo SQLAlchemy para el dominio de usuarios."""
import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    """Entidad ORM que representa un usuario registrado en el sistema."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relación con las tareas del usuario
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")  # type: ignore

