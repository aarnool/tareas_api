"""Módulo enrutador con endpoints para la gestión de tareas del usuario."""
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.orm import Session
from src.dependencies import get_current_user, get_db
from src.domains.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
import src.domains.tasks.service as task_service


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error / Error interno del servidor"
        }
    }
)


@router.post(
    "",
    summary="Create a new task / Crear una nueva tarea",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Task successfully created / Tarea creada exitosamente",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing or invalid authentication token / No autenticado"
        }
    }
)
def create_task(
    task: Annotated[TaskCreate, Body(description="The task information to create / La información de la tarea a crear")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    **Create Task / Crear Tarea**

    Creates a new task associated with the currently authenticated user.
    Crea una nueva tarea asociada al usuario actualmente autenticado.

    ### Details / Detalles:
    - **title**: Required task title / Título obligatorio de la tarea.
    - **status**: Default is `pending` (`in_progress`, `done`) / El estado por defecto es `pending`.
    - **priority**: Default is `medium` (`low`, `medium`, `high`) / Prioridad por defecto `medium`.
    """
    user_id = current_user["user_id"]
    return task_service.create_task(db, task, user_id)


@router.get(
    "",
    summary="Get all tasks / Obtener todas las tareas",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    response_description="List of user tasks / Lista de tareas del usuario",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing or invalid authentication token / No autenticado"
        }
    }
)
def get_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    start: Annotated[int | None, Query(
        description="The starting index for pagination / El índice de inicio para la paginación")] = 0,
    limit: Annotated[int | None, Query(
        description="The maximum number of tasks to retrieve / El número máximo de tareas a recuperar")] = 100):
    
    """
    **Retrieve User Tasks / Recuperar tareas del usuario**

    Returns a paginated list of all tasks owned by the currently authenticated user.
    Devuelve una lista paginada de todas las tareas pertenecientes al usuario autenticado.
    """
    user_id = current_user["user_id"]
    return task_service.get_all_tasks(db, user_id, start, limit)


@router.patch(
    "/{task_id}",
    summary="Update task by ID / Actualizar tarea por ID",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    response_description="Updated task information / Información actualizada de la tarea",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing or invalid authentication token / No autenticado"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found - Task does not exist or belongs to another user / Tarea no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Task not found/Tarea no encontrada"
                    }
                }
            }
        }
    }
)
def update_task(
    task_id: Annotated[int, Path(description="The ID of the task to update / El ID de la tarea a actualizar")],
    task_update: Annotated[TaskUpdate, Body(description="The updated task information / La información actualizada de la tarea")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """Actualiza parcialmente los campos de la tarea especificada por ID."""
    user_id = current_user["user_id"]
    return task_service.update_task(db, task_id, task_update, user_id)


@router.delete(
    "/{task_id}",
    summary="Delete task by ID / Eliminar tarea por ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing or invalid authentication token / No autenticado"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found - Task does not exist or belongs to another user / Tarea no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Task not found/Tarea no encontrada"
                    }
                }
            }
        }
    }
)
def delete_task(
    task_id: Annotated[int, Path(description="The ID of the task to delete / El ID de la tarea a eliminar")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
) -> None:
    """
    **Delete Task / Eliminar Tarea**

    Deletes a task by its ID. Only the task owner can delete it.
    Elimina una tarea por su ID. Solo el propietario de la tarea puede eliminarla.
    """
    user_id = current_user["user_id"]
    task_service.delete_task(db, task_id, user_id)