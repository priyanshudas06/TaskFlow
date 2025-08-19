from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    comment_text : str
    task_id: str
    user_id: str
    message: Optional[str] = None
    time_stamp: Optional[datetime] = datetime.now()