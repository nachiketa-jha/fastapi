import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, func
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):

    __tablename__ = "Posts"

    post_id = Column(Integer, primary_key=True)
    post_text = Column(String(255))
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())