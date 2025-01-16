from pydantic import BaseModel
from datetime import datetime

class RoleResponse(BaseModel):
    role_name: str
    updated_at: datetime
    created_at: datetime

    class Config:
       
        from_attributes = True