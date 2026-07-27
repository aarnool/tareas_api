from fastapi import APIRouter, status, Depends, Path, Body, Query
from sqlalchemy.orm import Session
from typing import Annotated
from src.dependencies import get_db, get_current_user
from src.domains.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate
import src.domains.tasks.service as task_service


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("",
    summary="Create a new task/Crear una nueva tarea",
    description="Create a new task with the provided information./Crear una nueva tarea con la información proporcionada.",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED)
def create_task(
    task: Annotated[TaskCreate, Body(description="The task information to create/La información de la tarea a crear")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]):
    
    user_id = current_user["user_id"]
    return task_service.create_task(db, task, user_id)


@router.get("",
    summary="Get all tasks/Obtener todas las tareas",
    description="Retrieve a list of all tasks./Recuperar una lista de todas las tareas.",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK)
def get_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    start: Annotated[int | None, Query(
        description="The starting index for pagination/El índice de inicio para la paginación")] = 0,
    limit: Annotated[int | None, Query( 
        description="The maximum number of tasks to retrieve/El número máximo de tareas a recuperar")] = 100):

    user_id = current_user["user_id"]
    return task_service.get_all_tasks(db, user_id, start, limit)


@router.patch("/{task_id}",
    summary="Update task by ID/Actualizar tarea por ID",
    description="Update a task's information by its unique ID./Actualizar la información de una tarea por su ID único.",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK)
def update_task(
    task_id: Annotated[int, Path(description="The ID of the task to update/El Id de la tarea a actualizar")],
    task_update: Annotated[TaskUpdate, Body(description="The updated task information/La información actualizada de la tarea")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]):

    user_id = current_user["user_id"]
    return task_service.update_task(db, task_id, task_update, user_id)


@router.delete("/{task_id}",
    summary="Delete task by ID/Eliminar tstmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)area por ID",
    description="Delete a task by its unique ID./Eliminar una tarea por su ID único.",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: Annotated[int, Path(description="The ID of the task to delete/El Id de la tarea a eliminar")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]) -> None:
    user_id = current_user["user_id"]
    task_service.delete_task(db, task_id, user_id)