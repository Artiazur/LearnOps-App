# Defines the Pydantic schemas used by the user module to validate input data
# and shape data exchanged between the API, application, and persistence layers.
# These schemas keep request/response contracts separate from the underlying
# database model, following the separation of concerns in Clean Architecture.

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
    ConfigDict
)
from datetime import date, datetime
from backend.src.modules.user.validators.password_validator import is_password_valid
from backend.src.shared.enum.user_roles import UserRole
import uuid


class UserBase(BaseModel):
    """Base schema containing the common fields shared across user schemas.

    Centralizing these fields avoids duplication between different user-related
    data contracts while allowing specialized schemas to extend the base model
    for specific use cases.
    """

    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserSignUp(UserBase):
    """Schema for validating user registration data.

    Extends the common user fields with password credentials and enforces the
    business rules required during registration, including password strength
    and confirmation matching.
    """

    password: str
    password_confirm: str

    @field_validator("password", mode="after")
    @classmethod
    def check_password(cls, value: str):
        """Validate the password against the application's password policy."""

        if not is_password_valid(value):
            raise ValueError(
                "Password is too weak"
            )
        return value

    @model_validator(mode="after")
    def check_password_match(self):
        """Ensure that the password confirmation matches the original password."""

        if self.password != self.password_confirm:
            raise ValueError(
                "Passwords do not match"
            )
        return self


class UserCreateInternal(UserBase):
    """Internal schema for creating a user after password processing.

    This schema is intended for the application layer after the plain-text
    password has been validated and hashed, ensuring that persistence-related
    operations receive the hashed credential rather than the original password.
    """

    hashed_password: str


class UserResponse(UserBase):
    """Schema defining the user data exposed by the application to API clients.

    It represents the public user contract and includes persisted user metadata
    while keeping internal authentication data, such as password hashes, out of
    API responses.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
    created_at: datetime
    is_active: bool
    role: UserRole = UserRole.STUDENT


class UserUpdate(BaseModel):
    """Schema for partial user profile updates.

    All fields are optional so the application can update only the attributes
    explicitly provided by the client without requiring the complete user
    profile.
    """

    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None