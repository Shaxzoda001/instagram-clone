from .database import Base, ENGINE
from .models import User, Post, Tags, Comments, Followers, Messages, PostTags, Likes

def migrate():
    Base.metadata.create_all(bind=ENGINE)