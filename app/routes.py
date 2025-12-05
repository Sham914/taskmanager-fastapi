from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserRead, TaskCreate, TaskRead
from .models import User, Task
from .db import get_db

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
# check if email exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="email already used")

    new_user = User(
        username=data.username,
        email=data.email,
        password=data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/tasks", response_model=TaskRead)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
    title=data.title,
    description=data.description,
    priority=data.priority,
    completed=False
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task