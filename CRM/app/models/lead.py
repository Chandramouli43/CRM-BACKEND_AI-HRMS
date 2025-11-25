from sqlalchemy import Column, Integer, String, Float, Date, Time, Text, Boolean, Enum, TIMESTAMP, func
from app.core.database import Base
import enum
from typing import Optional, List


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    value = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    status = Column(String, nullable=True)
    source = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    visibility = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# ---------------- PIPELINE MODEL ---------------- #
class StatusEnum(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
