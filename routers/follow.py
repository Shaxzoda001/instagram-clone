# routers/follow.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from models import User, Followers
from schemas.follow import FollowRequest
from database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/follow", status_code=201)
async def follow_user(follow_request: FollowRequest, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()

    following_id = follow_request.following_id

    if current_user_id == following_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")

    existing_follow = db.query(Followers).filter(
        Followers.follower_id == current_user_id,
        Followers.following_id == following_id
    ).first()

    if existing_follow:
        raise HTTPException(status_code=400, detail="You are already following this user.")

    target_user = db.query(User).filter(User.id == following_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found.")

    new_follow = Followers(follower_id=current_user_id, following_id=following_id)
    db.add(new_follow)
    db.commit()

    return jsonable_encoder({"detail": "Successfully followed the user."})

@router.delete("/unfollow", status_code=204)
async def unfollow_user(follow_request: FollowRequest, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()

    following_id = follow_request.following_id

    follow = db.query(Followers).filter(
        Followers.follower_id == current_user_id,
        Followers.following_id == following_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found.")

    db.delete(follow)
    db.commit()

    return jsonable_encoder({"detail": "Successfully unfollowed the user."})
