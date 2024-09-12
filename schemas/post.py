from pydantic import BaseModel
from typing import Optional

class CreatePostSchema(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]

class PostListSchema(BaseModel):
    pass

class PostUpdateSchema(BaseModel):
    pass
