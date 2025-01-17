from pydantic import BaseModel
from datetime import datetime

class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    is_admin: bool
    updated_at: datetime
    created_at: datetime

    class Config:
       
        from_attributes = True