# Defines FastAPI exception handlers for application-level authentication
# and user-related errors.
#
# This module belongs to the presentation/infrastructure boundary and is
# responsible for translating domain or application exceptions into HTTP
# responses. Keeping this translation here prevents API-specific response
# logic from leaking into application services and exception definitions.

from fastapi import Request, status
from fastapi.responses import JSONResponse
from backend.src.core.exceptions.token import (
    InvalidTokenError,
    TokenExpiredError,
    MissingRefreshTokenError
)
from backend.src.core.exceptions.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    EmptyUpdateError,
    UsernameAlreadyExistsError,
    UserNotFoundError
)
from backend.src.core.exceptions.redis_exc import RedisUnavailableError



async def token_error_handler(
    request: Request,
    exc: InvalidTokenError | TokenExpiredError
):
    """Convert token validation errors into a standardized HTTP 401 response.

    Both invalid and expired tokens are intentionally exposed through the same
    response to provide a consistent authentication error contract without
    revealing unnecessary details about token validation.
    """

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid or expired token."}
    )


async def missing_refresh_token_handler(
    request: Request,
    exc: MissingRefreshTokenError
):
    """Handle requests that do not provide a refresh token.

    Converts the missing refresh token exception into a standardized HTTP
    401 Unauthorized response for the API layer.
    """

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Refresh token is missing from the request."}
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError
):
    """Convert failed authentication attempts into an HTTP 401 response.

    The handler keeps credential-validation failures at the API boundary and
    prevents authentication services from depending on HTTP response objects.
    """

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials."}
    )


async def user_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):
    """Convert duplicate email registration errors into an HTTP 409 response."""

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User with this email already exists."}
    )


async def username_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError
):
    """Convert duplicate username errors into an HTTP 409 response."""

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Username already exists."}
    )


async def redis_connection_handler(
    request: Request,
    exc: RedisUnavailableError
):
    """Return a 503 response when Redis is unavailable."""
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Service temporarily unavailable."}
    )
    

async def empty_update_handler(
    request: Request,
    exc: EmptyUpdateError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "There is no data to update."}
    )
    
    
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
):
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "User not found."}
        )