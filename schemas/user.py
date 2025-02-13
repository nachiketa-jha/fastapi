import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, func
from pydantic import BaseModel
from database import Base


class User(Base):

    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True)
    uname = Column(String(30), unique=True)
    password = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
