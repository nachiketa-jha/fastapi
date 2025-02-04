from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    post_id: int
    post_text: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class CreatePostResponse(BaseModel):
    post_id: int
    post_text: str
    user_id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class UpdatePostResponse(BaseModel):
    post_id: int
    post_text: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

class GetPostResponse(BaseModel):
    post_id: int
    post_text: str
    user_id: int

    class Config:
        # orm_mode = True
        from_attributes = True

class GetPostByIDResponse(BaseModel):
    post_id: int
    post_text: str

    class Config:
        # orm_mode = True
        from_attributes = True