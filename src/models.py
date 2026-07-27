"""Módulo agregador que expone todos los modelos ORM de los dominios."""
from src.domains.users.models import User
from src.domains.tasks.models import Task

__all__ = ["User", "Task"]