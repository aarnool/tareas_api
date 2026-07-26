from fastapi import APIRouter, status, HTTPException, Depends, Path, Body, Query
from sqlalchemy.orm import Session, session
from sqlalchemy import select
from typing import Annotated
from src.domains.tasks.dependencies import get_db, get_current_user
from src.domains.tasks.models import Task, TaskStatus, TaskPriority
from src.domains.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate
from src.domains.users.models import User


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
    
    # Check if the user exists
    user_id = current_user["user_id"]
    # Create a new task instance

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


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
    tasks = db.query(Task).filter(Task.user_id == user_id).offset(start).limit(limit).all()
    return tasks


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
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db.scalar(stmt)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found/Tarea no encontrada"
        )
    
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}",
    summary="Delete task by ID/Eliminar tstmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)area por ID",
    description="Delete a task by its unique ID./Eliminar una tarea por su ID único.",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: Annotated[int, Path(description="The ID of the task to delete/El Id de la tarea a eliminar")],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]) -> None:
    user_id = current_user["user_id"]
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db.scalar(stmt)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found/Tarea no encontrada"
        )
    
    db.delete(task)
    db.commit()
    