from fastapi import APIRouter, Depends, status, HTTPException
from database import ENGINE, Session
from models import Post, User
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from schemas.post import CreatePostSchema
from sqlalchemy import or_

session = Session(bind=ENGINE)

post_router = APIRouter(prefix="/post", tags=["post"])


@post_router.get("/")
async def get_post(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )
        ).first()
        if current_user:
            posts = session.query(Post).filter(Post.user == current_user).all()
            return jsonable_encoder(posts)
    except HTTPException:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@post_router.post("/")
async def create_post(post: CreatePostSchema, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = (session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )).first())
        if current_user:
            new_posts = Post(
                image_path=post.image_path,
                caption=post.caption
            )
            new_posts.user = current_user
            session.add(new_posts)
            session.commit()
            data = {
                "success": True,
                "code": 200,
                "messages": f"Posts {authorization.get_jwt_subject()} ",
            }
            return jsonable_encoder(data)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
