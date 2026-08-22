# Defines the HTTP endpoints for the authentication module.
# This module belongs to the presentation/API layer of the Clean Architecture.
# It is responsible for receiving authentication requests, resolving
# application dependencies, and translating authentication results into API
# responses. Authentication logic itself remains inside AuthService.

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend.src.modules.auth.schemas.login import LoginSchema
from backend.src.modules.auth.schemas.response import LoginResponse
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.modules.user.models.user_model import UserModel
from backend.src.shared.dependencies.user import get_auth_service, get_current_user
from backend.src.core.exceptions.user import InvalidCredentialsError, UserNotFoundError
from backend.src.core.exceptions.token import InvalidTokenError, TokenExpiredError


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    data: LoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Authenticate a user and return the issued authentication tokens.

    The endpoint delegates credential validation and token generation to
    AuthService, keeping authentication logic out of the API layer.
    """

    access_token, refresh_token = await service.login(
        email=data.email,
        password=data.password
    )

    # Temporary response implementation.
    # Tokens will be moved to a secure transport mechanism once the
    # authentication flow is finalized.

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/test-auth")
async def test_auth(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Verify that the current request contains a valid authenticated user.

    This endpoint is intended as a temporary authentication-flow check and
    relies on the current-user dependency to validate the request token and
    resolve the authenticated user.
    """

    return {
        "message": "It works!",
        "user_id": str(current_user.id)
    }