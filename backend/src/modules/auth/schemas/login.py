# Defines the input schema for the user login flow.
# This schema belongs to the presentation/API contract layer and is responsible
# for validating the credentials received from the client before they are
# passed to the authentication application service.

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    """Represents the credentials required to authenticate a user.

    Pydantic validates the email format before the credentials enter the
    application layer, while password verification is handled by the
    authentication service through the password-hashing abstraction.
    """

    email: EmailStr
    password: str
