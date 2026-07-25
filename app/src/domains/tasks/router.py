from fastapi import APIRouter, status, HTTPException, Depends, Path, Body, Query
from sqlalchemy.orm import Session
from typing import Annotated
from app.src.domains.tasks.dependencies import get_db
from app.src.domains.tasks.models import Task, TaskStatus, TaskPriority
from app.src.domains.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate
from app.src.domains.users.models import User


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
    db: Annotated[Session, Depends(get_db)]):
    
    # Check if the user exists
    user = db.get(User, task.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found/Usuario no encontrado"
        )

    # Create a new task instance

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        user_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{task_id}",
    summary="Get task by ID/Obtener tarea por ID",
    description="Retrieve a task by its unique ID./Recuperar una tarea por su ID único.",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK)
def get_task_by_id(
    task_id: Annotated[int, Path(description="The ID of the task to retrieve/El Id de la tarea a recuperar")],
    db: Annotated[Session, Depends(get_db)]):
    
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found/Tarea no encontrada"
        )
    return task

@router.get("",
    summary="Get all tasks/Obtener todas las tareas",
    description="Retrieve a list of all tasks./Recuperar una lista de todas las tareas.",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK)
def get_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    start: Annotated[int | None, Query(
        description="The starting index for pagination/El índice de inicio para la paginación")] = 0,
    limit: Annotated[int | None, Query( 
        description="The maximum number of tasks to retrieve/El número máximo de tareas a recuperar")] = 100):
    
    tasks = db.query(Task).offset(start).limit(limit).all()
    return tasks


@router.patch("/{task_id}",
    summary="Update task by ID/Actualizar tarea por ID",
    description="Update a task's information by its unique ID./Actualizar la información de una tarea por su ID único.",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK)
def update_task(
    task_id: Annotated[int, Path(description="The ID of the task to update/El Id de la tarea a actualizar")],
    task_update: Annotated[TaskUpdate, Body(description="The updated task information/La información actualizada de la tarea")],
    db: Annotated[Session, Depends(get_db)]):
    
    task = db.get(Task, task_id)
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
    summary="Delete task by ID/Eliminar tarea por ID",
    description="Delete a task by its unique ID./Eliminar una tarea por su ID único.",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: Annotated[int, Path(description="The ID of the task to delete/El Id de la tarea a eliminar")],
    db: Annotated[Session, Depends(get_db)]):
    
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found/Tarea no encontrada"
        )
    
    db.delete(task)
    db.commit()
    return {
        "detail": "Task deleted successfully/Tarea eliminada con éxito"
    }