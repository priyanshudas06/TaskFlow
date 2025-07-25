from pydantic import BaseModel
from typing import Optional, List

class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = ""