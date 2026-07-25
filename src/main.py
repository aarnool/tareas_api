from fastapi import FastAPI
from src.database import engine, Base
from src.models import User, Task

from src.domains.users.router import router as user_router
from src.domains.tasks.router import router as task_router

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(user_router)
app.include_router(task_router)