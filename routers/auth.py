import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import User
from schemas.auth import RegisterSchema, LoginSchema, PasswordResetSchema
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def get_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

    return {"message": "auth page"}

@auth_router.post('/login', status_code=200)
async def login_user(user: LoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    check_user = db.query(User).filter(User.username == user.username).first()
    if check_user and check_password_hash(check_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=10)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=check_user.username, expires_time=refresh_lifetime)
        return jsonable_encoder({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

@auth_router.post('/register')
async def register_user(user: RegisterSchema, db: Session = Depends(get_db)):
    check_user = db.query(User).filter(User.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return jsonable_encoder({"status": 201, "success": True, "message": "User registered"})

@auth_router.get('/users')
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return jsonable_encoder(users)

@auth_router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        access_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        check_user = db.query(User).filter(User.username == current_user).first()
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        new_access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)
        return jsonable_encoder({
            "code": 200,
            "success": True,
            "message": "New access token created",
            "data": new_access_token
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@auth_router.post("/reset-password")
async def reset_password(user: PasswordResetSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
        if user.password == user.correct_password:
            current_user = db.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
            if current_user:
                current_user.password = generate_password_hash(user.password)
                db.add(current_user)
                db.commit()
                return jsonable_encoder({"success": True, "code": 200, "message": "Password successfully updated"})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or credentials")
