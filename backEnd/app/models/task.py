from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    decription: Optional[str] =""
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    status: str = "pending"
    board_id: str