from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.models import Task, ActivityLog
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskOut
from app.utils.auth import get_current_user, require_admin
from app.models.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        created_by=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    log = ActivityLog(
        user_id=current_user.id,
        action="task_created",
        details=f"Task '{task.title}' created"
    )
    db.add(log)
    db.commit()
    return {"message": "Task created", "task_id": new_task.id}

@router.get("/")
def get_tasks(
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    tasks = query.all()
    return tasks

@router.patch("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")
    task.status = task_update.status
    db.commit()
    log = ActivityLog(
        user_id=current_user.id,
        action="task_updated",
        details=f"Task {task_id} updated to {task_update.status}"
    )
    db.add(log)
    db.commit()
    return {"message": "Task updated successfully"}