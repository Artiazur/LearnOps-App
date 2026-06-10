from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Annotated
from datetime import date
from src.core.exceptions import WeakPasswordError
from src.modules.user.validators.password_validator import is_password_valid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserSignUp(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=16)]
    password_confirm: str

    @field_validator("password", mode="after")
    @classmethod
    def check_password(cls, value: str):
        if not is_password_valid(value):
            raise ValueError(
                "Password is too weak"
            )
        return value

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.password_confirm:
            raise ValueError(
                "Passwords do not match"
            )
        return self

class UserResponse(UserBase):
    id: int
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
    created_at: date
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
