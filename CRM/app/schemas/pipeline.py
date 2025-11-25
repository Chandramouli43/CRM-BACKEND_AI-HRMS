from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime, time
from enum import Enum as PyEnum

from pydantic import BaseModel
from datetime import date
from enum import Enum as PyEnum

class StatusEnum(str, PyEnum):
    active = "Active"
    inactive = "Inactive"

class PipelineBase(BaseModel):
    pipeline_Name: str
    total_deal_value: float
    deals: int
    stages: str
    created_date: date
    status: StatusEnum

class PipelineCreate(PipelineBase):
    pass

class PipelineResponse(PipelineBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
