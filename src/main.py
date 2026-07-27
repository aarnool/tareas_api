"""Punto de entrada principal de la aplicación FastAPI y registro de enrutadores."""
from fastapi import FastAPI
from src.domains.tasks.router import router as task_router
from src.domains.users.router import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173",
    settings.FRONTEND_URL  # Agrega la URL del frontend desde la configuración
    ]



app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(user_router)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)