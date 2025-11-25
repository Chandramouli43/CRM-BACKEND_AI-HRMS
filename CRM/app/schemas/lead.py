from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# ---------------- LEAD SCHEMAS ---------------- #

class LeadBase(BaseModel):
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    industry: Optional[str] = None
    owner: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None

    model_config = {"from_attributes": True}


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------- ANALYTICS SCHEMAS ---------------- #

class StageSummary(BaseModel):
    stage_name: str
    total_deals: int

    model_config = {"from_attributes": True}


class SourceBreakdown(BaseModel):
    source_name: str
    total_leads: int

    model_config = {"from_attributes": True}
