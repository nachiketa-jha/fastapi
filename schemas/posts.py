from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    post_text: str
    updated_at: datetime
    created_at: datetime

    class Config:
       
        from_attributes = True