from pydantic import BaseModel
from datetime import datetime

class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    is_admin: bool
    updated_at: datetime
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class CreateRoleResponse(BaseModel):
    role_id: int
    role_name: str
    is_admin: bool
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class UpdateRoleResponse(BaseModel):
    role_id: int
    role_name: str
    is_admin: bool
    updated_at: datetime
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class GetRoleResponse(BaseModel):
    role_id: int
    role_name: str
    is_admin: bool

    class Config:
        # orm_mode = True
        from_attributes = True