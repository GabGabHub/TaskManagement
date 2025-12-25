from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str
    status: str = "open"
    priority: str
    assignedTo: Optional[str] = None
    createdAt: Optional[datetime] = None
    assignedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None

class User(BaseModel):
    username: str
    role: str = "user"
    joinedAt: Optional[datetime] = None