import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from uuid import UUID
from models import Comments, User, Post
from schemas.comments import CommentCreate, Comment
from database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# Dependency for JWT authentication
def get_current_user(Authorize: AuthJWT = Depends()) -> User:
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    db = next(get_db())
    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/comments/", response_model=Comment)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_comment = Comments(
        user_id=current_user.id,
        post_id=comment.post_id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return jsonable_encoder(db_comment)

@router.get("/comments/{comment_id}", response_model=Comment)
def read_comment(comment_id: str, db: Session = Depends(get_db)):
    comment = db.query(Comments).filter(Comments.id == UUID(comment_id)).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return jsonable_encoder(comment)

@router.put("/comments/{comment_id}", response_model=Comment)
def update_comment(comment_id: str, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = db.query(Comments).filter(Comments.id == UUID(comment_id)).first()
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")

    db_comment.content = comment.content
    db_comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_comment)
    return jsonable_encoder(db_comment)

@router.delete("/comments/{comment_id}", response_model=Comment)
def delete_comment(comment_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = db.query(Comments).filter(Comments.id == UUID(comment_id)).first()
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")

    db.delete(db_comment)
    db.commit()
    return jsonable_encoder(db_comment)
