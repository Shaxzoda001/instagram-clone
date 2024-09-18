import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_app.app.schema import LoginSchema, RegisterSchema, ResetPasswordSchema
from fastapi_app.app.database import ENGINE, Session
from fastapi_app.app.models import User
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def auth():
    return {"message": "Auth router"}


@auth_router.post("/login")
async def auth_login_user(request: LoginSchema, authorization: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == request.username_or_email,
            User.email == request.username_or_email
        )
    ).first()
    if check_user is not None:
        if check_password_hash(check_user.password, request.password):
            access_token = authorization.create_access_token(subject=request.username_or_email, expires_time=datetime.timedelta(minutes=1))
            refresh_token = authorization.create_access_token(subject=request.username_or_email, expires_time=datetime.timedelta(days=1))
            response = {
                "status_code": 200,
                "access_toke": access_token,
                "refresh_token": refresh_token,
                "detail": "Login successfully"
            }
            return jsonable_encoder(response)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password or username")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.post("/register")
async def auth_register_user(request: RegisterSchema):
    try:
        check_user = session.query(User).filter(
            or_(
                User.username == request.username,
                User.email == request.email
            )
        ).first()
        if check_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        new_user = User(
            username=request.username,
            email=request.email,
            password=generate_password_hash(request.password)
        )
        session.add(new_user)
        session.commit()
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="User registered")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")


@auth_router.get('/token/verify')
async def verify_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token already or invalid")
    return {"status": "Token is valid"}


@auth_router.get("/users")
async def users():
    users = session.query(User).all()
    return users











