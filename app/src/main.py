from fastapi import FastAPI
from app.src.database import engine, Base
from app.src.domains.users import models as user_models
from app.src.domains.tasks import models as task_models

from app.src.domains.users.router import router as user_router
from app.src.domains.tasks.router import router as task_router

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(user_router)
app.include_router(task_router)