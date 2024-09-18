from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from models import Likes, Post
from schemas.like import LikeSchema
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LikeResponse(BaseModel):
    post_id: UUID
    detail: str

@router.post("/like", status_code=status.HTTP_201_CREATED)
def add_like(like_request: LikeSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Authenticate the user
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    # Check if the post exists
    post = db.query(Post).filter(Post.id == like_request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check if the user already liked the post
    existing_like = db.query(Likes).filter(Likes.post_id == like_request.post_id, Likes.user_id == current_user).first()
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this post")

    # Create a new like
    new_like = Likes(user_id=current_user, post_id=like_request.post_id)
    db.add(new_like)
    db.commit()

    response = LikeResponse(post_id=like_request.post_id, detail="Like added successfully")
    return jsonable_encoder(response)

@router.delete("/like/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(post_id: UUID, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Authenticate the user
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    # Check if the like exists
    like = db.query(Likes).filter(Likes.post_id == post_id, Likes.user_id == current_user).first()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")

    # Remove the like
    db.delete(like)
    db.commit()

    response = LikeResponse(post_id=post_id, detail="Like removed successfully")
    return jsonable_encoder(response)
