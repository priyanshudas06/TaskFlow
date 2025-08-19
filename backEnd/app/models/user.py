from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from .task import TaskOut

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str = Field(..., alias="id")
    email: EmailStr
    full_name: Optional[str] = None
    username: str

    class Config:
        validate_by_name = True

class UserProfileWithTasks(UserResponse):
    tasks: List[TaskOut] = []

class RefreshTokenResponse(BaseModel):
    refresh_token: str  