"""Punto de entrada principal de la aplicación FastAPI y registro de enrutadores."""
from fastapi import FastAPI
from src.domains.tasks.router import router as task_router
from src.domains.users.router import router as user_router

app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(user_router)
app.include_router(task_router)