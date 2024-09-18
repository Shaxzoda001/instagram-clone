from pydantic import BaseModel
from typing import Optional


class LoginSchema(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username_or_phone_number": None,
                "password": None
            }
        }


class RegisterSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]


class ResetPasswordSchema(BaseModel):
    password: Optional[str]
    password2: Optional[str]


class ConfigBase(BaseModel):
    authjwt_secret_key: str = "secret_token"
