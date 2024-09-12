from fastapi import FastAPI, status, Depends, HTTPException
from database import Session, ENGINE
from models import User
from routers.auth import auth_router
from routers.post import post_router
from routers.like import like_router
from routers.comments import comments_router
from routers.follow import follow_router
from schemas.auth import Settings
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_

app = FastAPI()
session = Session(bind=ENGINE)


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comments_router)
app.include_router(follow_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


@like_router.get("/posts/{username}")
async def get_user_page(username: str, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user:
            other_user = session.query(User).filter(User.username == username).first()
            if other_user:
                data = {
                    "success": True,
                    "code": 200,
                    "message": f"{other_user.username} profile view"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} not found")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
