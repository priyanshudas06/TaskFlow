from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    decription: Optional[str] =""
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    status: str = "pending"
    board_id: str
    priority: Optional[str] = "medium"
    created_by: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = []
    is_completed: bool = False
