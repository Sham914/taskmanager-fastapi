from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id:int
    username: str
    email: str

class TaskCreate(BaseModel):
    title: str
    description: str
    priority:int

class TaskRead(BaseModel):
    id:int
    title:str
    description:str
    priority: int
    completed: bool