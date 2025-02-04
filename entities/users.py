from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    user_id: int
    uname: str
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class GetUserResponse(BaseModel):
    user_id: int
    uname: str


    class Config:
        orm_mode = True
        from_attributes = True

class CreateUserResponse(BaseModel):
    user_id: int
    uname: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class UpdateUserResponse(BaseModel):
    user_id: int
    uname: str
    password: str
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class LoginUserResponse(BaseModel):
    user_id: int
    password: str

    class Config:
        from_attributes = True