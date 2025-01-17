from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    username: str
    user_id: int
    password: str | None = None
    updated_at: datetime
    created_at: datetime

    class Config:
       
        from_attributes = True
        json_encoders = {
            "password": lambda v: None
        }