import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, func
from pydantic import BaseModel
from database import Base

class Role(Base):
    __tablename__ = "Roles"

    role_id = Column(Integer,primary_key=True)
    role_name = Column(String(30))
    is_admin = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())