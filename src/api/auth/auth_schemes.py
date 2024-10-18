from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import re

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str



# Pydantic Model for User Registration
class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    disabled: Optional[bool] = False

    @staticmethod
    def validate_password(password: str):
        # Custom validation for strong password
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character.")

        return password
