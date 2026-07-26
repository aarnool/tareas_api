from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.domains.tasks.models import Task
from src.domains.tasks.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
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


def get_all_tasks(db: Session, user_id: int, start: int | None = 0, limit: int | None = 100) -> list[Task]:
    tasks = db.query(Task).filter(Task.user_id == user_id).offset(start).limit(limit).all()
    return tasks


def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Task:
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


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db.scalar(stmt)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found/Tarea no encontrada"
        )
    
    db.delete(task)
    db.commit()
