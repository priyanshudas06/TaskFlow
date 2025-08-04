from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    # id: Optional[str] = None
    title: str
    decription: Optional[str] =""
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    status: str = "pending"
    board_id: str
    priority: Optional[str] = "medium"
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    is_completed: bool = False

class TaskOut(TaskCreate):
    task_id: str
    user_id: str