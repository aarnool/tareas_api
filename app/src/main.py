from fastapi import FastAPI
from app.src.database import engine, Base
from app.src.domains.users import models as user_models
from app.src.domains.tasks import models as task_models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.0.0")