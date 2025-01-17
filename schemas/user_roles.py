from pydantic import BaseModel
from datetime import datetime

class UserRoleResponse(BaseModel):
    user_role_id: int
    user_id: int
    role_id:int
    updated_at: datetime
    created_at: datetime

    class Config:
       
        from_attributes = True