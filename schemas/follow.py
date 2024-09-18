from pydantic import BaseModel
from typing import Optional
import uuid

class FollowRequest(BaseModel):
    following_id: uuid.UUID
