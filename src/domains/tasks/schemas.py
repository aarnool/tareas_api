"""Módulo de esquemas Pydantic para la validación y serialización de tareas."""
from datetime import datetime
from pydantic import BaseModel, Field
from src.domains.tasks.models import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    """Esquema base con atributos comunes de las tareas."""
    title: str = Field(
        description="The title of the task/El título de la tarea",
        examples=["Comprar suministros"]
    )
    description: str | None = Field(
        default=None,
        description="The description of the task/La descripción de la tarea",
        examples=["Ir al supermercado a comprar café y leche"]
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="The status of the task/El estado de la tarea",
        examples=[TaskStatus.PENDING]
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="The priority of the task/La prioridad de la tarea",
        examples=[TaskPriority.MEDIUM]
    )


class TaskCreate(TaskBase):
    """Esquema para la petición de creación de una nueva tarea."""
    pass


class TaskUpdate(BaseModel):
    """Esquema para la actualización parcial o total de una tarea."""
    title: str | None = Field(
        default=None,
        description="The title of the task/El título de la tarea",
        examples=["Comprar suministros urgentes"]
    )
    description: str | None = Field(
        default=None,
        description="The description of the task/La descripción de la tarea",
        examples=["Ir al supermercado antes de las 8 PM"]
    )
    status: TaskStatus | None = Field(
        default=None,
        description="The status of the task/El estado de la tarea",
        examples=[TaskStatus.IN_PROGRESS]
    )
    priority: TaskPriority | None = Field(
        default=None,
        description="The priority of the task/La prioridad de la tarea",
        examples=[TaskPriority.HIGH]
    )


class TaskResponse(TaskBase):
    """Esquema de respuesta devuelto al cliente con la información completa de la tarea."""
    id: int = Field(
        description="The unique identifier of the task/El identificador único de la tarea",
        examples=[1]
    )
    created_at: datetime = Field(
        description="The timestamp when the task was created/La marca de tiempo cuando se creó la tarea"
    )
    updated_at: datetime | None = Field(
        default=None,
        description="The timestamp when the task was last updated/La marca de tiempo cuando se actualizó por última vez la tarea"
    )

    model_config = {
        "from_attributes": True,
    }