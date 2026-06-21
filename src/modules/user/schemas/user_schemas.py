from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
    ConfigDict
)
from datetime import date, datetime
from src.modules.user.validators.password_validator import is_password_valid
from src.shared.enum.user_roles import UserRole
import uuid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserSignUp(UserBase):
    password: str
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


class UserCreateInternal(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
    created_at: datetime
    is_active: bool
    role: UserRole = UserRole.STUDENT

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
