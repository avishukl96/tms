from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "To-do"
    assigned_to: Optional[int] = None
    admin_id: int  # Admin ID required for task assignment

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: int
