from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .schemas import UserCreate, UserRead, TaskCreate, TaskRead
from .models import User, Task
from .db import get_db
from .security import (
hash_password,
verify_password,
create_access_token,
decode_access_token,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/users", response_model=UserRead)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="email already used")

    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
def login(
form_data: OAuth2PasswordRequestForm = Depends(),
db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="invalid credentials")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
def get_current_user(
token: str = Depends(oauth2_scheme),
db: Session = Depends(get_db),
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not found")

    return user

@router.post("/tasks", response_model=TaskRead)
def create_task(
data: TaskCreate,
db: Session = Depends(get_db),
current_user=Depends(get_current_user),
):
    new_task = Task(
    title=data.title,
    description=data.description,
    priority=data.priority,
    completed=False,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks", response_model=list[TaskRead])
def list_tasks(
db: Session = Depends(get_db),
current_user=Depends(get_current_user),
):
    tasks = db.query(Task).all()
    return tasks