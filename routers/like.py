from fastapi import APIRouter, Depends, status, HTTPException
from database import ENGINE, Session
from models import Likes, User, Post
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_

like_router = APIRouter(prefix="/like", tags=["likes"])

session = Session(bind=ENGINE)


@like_router.get('/')
async def get_like(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user is not None:
            likes = session.query(Likes).filter(Likes.user == current_user.id).all()
            data = {
                "success": True,
                "code": 200,
                "message": f"All posts {current_user.username} likes",
                "likes": likes
            }
            return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})



