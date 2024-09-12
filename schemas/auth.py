from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]

class Settings(BaseModel):
    authjwt_secret_key: str = "0c8f2d8abe22878f3880aafdde57c0a3e4c58eac7cf75a08c9972b86c64ead10"

class LoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

class PasswordResetSchema(BaseModel):
    password: Optional[str]
    confirm_password: Optional[str]
