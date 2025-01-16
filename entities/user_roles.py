import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, func
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from database import Base

class UserRole(Base):
    __tablename__ = "UserRoles"

    user_role_id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    role_id = Column(Integer, ForeignKey("Roles.role_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())