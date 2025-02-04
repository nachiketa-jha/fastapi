from pydantic import BaseModel
from datetime import datetime

class UserRoleResponse(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class GetUserRoleResponse(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int

    class Config:
        # orm_mode = True
        from_attributes = True

class CreateUserRoleResponse(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class UpdateUserRoleResponse(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int
    updated_at: datetime


    class Config:
        # orm_mode = True
        from_attributes = True