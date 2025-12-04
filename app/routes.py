from fastapi import APIRouter, HTTPException
from .schemas import UserCreate, UserRead, TaskCreate, TaskRead

router = APIRouter()

fake_users = []
fake_tasks = []
user_id_counter = 1
task_id_counter = 1

@router.post("/users", response_model=UserRead)
def create_user(data: UserCreate):
    global user_id_counter
    # check duplicate email
    for u in fake_users:
        if u["email"] == data.email:
            raise HTTPException(status_code=400, detail="email already used")

    new_user = {
        "id": user_id_counter,
        "username": data.username,
        "email": data.email
    }
    fake_users.append(new_user)
    user_id_counter += 1
    return new_user

@router.post("/tasks", response_model=TaskRead)
def create_task(data: TaskCreate):
    global task_id_counter
    new_task = {
        "id": task_id_counter,
        "title": data.title,
        "description": data.description,
        "priority": data.priority,
        "completed": False
    }
    fake_tasks.append(new_task)
    task_id_counter += 1
    return new_task
