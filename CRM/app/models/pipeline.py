from sqlalchemy import Column, Integer, String, Float, Date, Time, Text, Boolean, Enum, TIMESTAMP, func
from app.core.database import Base
import enum
from typing import Optional, List


class StatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_Name = Column(String, nullable=False)
    total_deal_value = Column(Float, nullable=False)
    deals = Column(Integer, nullable=False)
    stages = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.active)


# ---------------- ACTIVITY MODEL ---------------- #
