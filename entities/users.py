import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, func
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from database import Base


class User(Base):

    __tablename__ = "Users"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())