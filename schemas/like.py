from pydantic import BaseModel
from uuid import UUID

class LikeSchema(BaseModel):
    post_id: UUID
