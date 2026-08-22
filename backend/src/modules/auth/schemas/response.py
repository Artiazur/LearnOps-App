# Defines the Pydantic response schema for the authentication login flow.
# This schema belongs to the presentation/API contract layer and determines
# the structure of the data returned to the client after successful
# authentication.

from pydantic import BaseModel


class LoginResponse(BaseModel):
    """Represents the response returned after a successful user login.

    The response contains a human-readable message together with the access
    and refresh tokens required by the client to authenticate subsequent
    requests and obtain new access tokens.
    """

    message: str = ""
    access_token: str
    refresh_token: str
