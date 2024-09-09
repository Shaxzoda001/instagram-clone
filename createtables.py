from database import Base, ENGINE
from models import User, Post, Comments, Likes, Followers, PostTags, Messages

if __name__ == '__main__':
    Base.metadata.create_all(bind=ENGINE)
