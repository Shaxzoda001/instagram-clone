from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: str
    user_id: str
    post_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
