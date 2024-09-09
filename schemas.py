from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]

class Settings(BaseModel):
    authjwt_secret_key: str = "9966cbd750715bccdca258c682d363a2253ec8cc3f344d4c45ee07f455894cbb"

class UserLogin(BaseModel):
    username: Optional[str]
    password: Optional[str]

class UserPasswordReset(BaseModel):
    password: Optional[str]
    confirm_password: Optional[str]
