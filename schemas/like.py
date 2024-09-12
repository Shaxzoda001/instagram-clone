from pydantic import BaseModel
from typing import Optional


class LikeCreateSchema(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]