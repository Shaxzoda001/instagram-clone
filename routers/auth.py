import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import User
from schemas.auth import RegisterSchema, LoginSchema, PasswordResetSchema
from database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_


session = Session(bind=ENGINE)

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def get_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

    return HTTPException(status_code=status.HTTP_200_OK, detail="auth page")

@auth_router.post('/login', status_code=200)
async def login_user(user: LoginSchema, Authorize: AuthJWT = Depends()):
    # check_user = session.query(User).filter(User.username == user.username).first()
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user:
        if check_password_hash(check_user.password, user.password):
            access_lifetime = datetime.timedelta(minutes=10)
            refresh_lifetime = datetime.timedelta(days=3)
            access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)
            refresh_token = Authorize.create_refresh_token(subject=check_user.username, expires_time=refresh_lifetime)
            token = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "token": token
            }
            return jsonable_encoder(response)
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

@auth_router.post('/register')
async def register_user(user: RegisterSchema):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "success": True,
        "message": "User registered"
    }
    return jsonable_encoder(data)


@auth_router.get('/users')
async def get_users():
    users = session.query(User).all()
    return jsonable_encoder(users)

@auth_router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        access_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        check_user = session.query(User).filter(User.username == current_user).first()
        if check_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        new_access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)

        response = {
            "code": 200,
            "success": True,
            "message": "New refresh token created",
            "data": new_access_token
        }
        return jsonable_encoder(response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@auth_router.post("/reset-password")
async def reset_password(user: PasswordResetSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        if user.password ==user.correct_password:
            current_user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
            if current_user:
                current_user.password = generate_password_hash(user.password)
                session.add(current_user)
                session.commit()
                data = {
                    "success": True,
                    "code": 200,
                    "message": "Password changes successfully done"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials or invalid token")












