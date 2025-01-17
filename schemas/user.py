from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    username: str
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None  # Optional for newly created users

    class Config:
        from_attributes = True