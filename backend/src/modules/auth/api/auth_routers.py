# Defines the HTTP endpoints for the authentication module.
# This module belongs to the presentation/API layer of the Clean Architecture.
# It is responsible for receiving authentication requests, resolving
# application dependencies, and translating authentication results into API
# responses. Authentication logic itself remains inside AuthService.

from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from backend.src.modules.auth.schemas.login import LoginSchema
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.modules.user.models.user_model import UserModel
from backend.src.core.exceptions.token import MissingRefreshTokenError
from backend.src.shared.dependencies.user import (
    get_auth_service,
    get_current_user,
    get_refresh_token_repo
) 


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    data: LoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> JSONResponse:
    """Authenticate a user and return the issued authentication tokens.

    The endpoint delegates credential validation and token generation to
    AuthService, keeping authentication logic out of the API layer.
    """

    access_token, refresh_token = await service.login(
        email=data.email,
        password=data.password
    )

    response = JSONResponse(
        content={"access_token": access_token}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True
    )

    return response


@router.post("/refresh")
async def refresh(
    request: Request,
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> JSONResponse:
    """Refresh the user's authentication tokens.

    The refresh token is retrieved from the HTTP-only cookie and delegated to
    the authentication service for validation and token rotation. The new
    access token is returned in the response body, while the rotated refresh
    token is stored in a new HTTP-only cookie.

    Token validation and rotation remain within the application service,
    keeping the API layer focused on HTTP-specific responsibilities.
    """

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise MissingRefreshTokenError()

    new_access_token, new_refresh_token = await service.refresh(
        refresh_token=refresh_token
    )

    response = JSONResponse(
        content={"access_token": new_access_token}
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True
    )

    return response


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


