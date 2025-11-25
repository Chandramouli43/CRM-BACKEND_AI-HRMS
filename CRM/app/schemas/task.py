# app/schemas/task.py
from datetime import date
from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    completed: Optional[bool] = False

    model_config = {"extra": "ignore"}


class TaskCreate(TaskBase):
    # allow sending projected time parts from client when creating
    projected_days: Optional[int] = 0
    projected_hours: Optional[int] = 0
    projected_minutes: Optional[int] = 0


class TaskUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    projected_days: Optional[int]
    projected_hours: Optional[int]
    projected_minutes: Optional[int]
    completed: Optional[bool]

    model_config = {"extra": "ignore"}


class TaskInDBBase(TaskBase):
    id: int
    # expose the DB total-minutes value as projected_minutes_total
    projected_minutes_total: int = 0

    model_config = {
        "from_attributes": True,   # for pydantic v2; allows reading from ORM attributes
    }


class Task(TaskInDBBase):
    pass
