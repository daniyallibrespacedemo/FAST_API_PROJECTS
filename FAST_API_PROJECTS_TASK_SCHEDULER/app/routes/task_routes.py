from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.task_schema import TaskCreate
from app.dependencies import get_db
from app.models.task import Task

router = APIRouter(prefix='/tasks')

@router.post('/')
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=1
    )

    db.add(new_task)
    db.commit()

    return {"message":"Task Created"}

@router.get('/')
def get_tasks(db:Session=Depends(get_db)):
    tasks = db.query(Task)
    return tasks

@router.delete('/{task_id}')
def delete_task(task_id: int, db:Session=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    db.delete(task)
    db.commit()

    return {"message":f"Task with id [{task_id}] deleted."}