from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.src.database import Base
from sqlalchemy import String, Integer, DateTime, func
import datetime
from app.src.domains.tasks.models import Task

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationship to the Task model
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
