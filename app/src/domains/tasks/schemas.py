from pydantic import BaseModel, Field
from app.src.domains.tasks.models import TaskStatus, TaskPriority
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(
        description="The title of the task/El título de la tarea")
    description: str | None = Field(
        default=None, 
        description="The description of the task/La descripción de la tarea")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, 
        description="The status of the task/El estado de la tarea")
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, 
        description="The priority of the task/La prioridad de la tarea")
    user_id: int = Field(
            description="The ID of the user who owns the task/El ID del usuario que posee la tarea")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None, 
        description="The title of the task/El título de la tarea")
    description: str | None = Field(
        default=None, 
        description="The description of the task/La descripción de la tarea")
    status: TaskStatus | None = Field(
        default=None, 
        description="The status of the task/El estado de la tarea")
    priority: TaskPriority | None = Field(
        default=None, 
        description="The priority of the task/La prioridad de la tarea")

class TaskResponse(TaskBase):
    id: int = Field(
        description="The unique identifier of the task/El identificador único de la tarea")
    created_at: datetime = Field(
        description="The timestamp when the task was created/La marca de tiempo cuando se creó la tarea")
    updated_at: datetime | None = Field(
        default=None, 
        description="The timestamp when the task was last updated/La marca de tiempo cuando se actualizó por última vez la tarea")

    model_config = {
        "from_attributes": True,
    }