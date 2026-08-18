from fastapi import Request, status
from fastapi.responses import JSONResponse
from backend.src.core.exceptions.token import (
    InvalidTokenError,
    TokenExpiredError
)
from backend.src.core.exceptions.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UsernameAlreadyExistsError
)


async def token_error_handler(
    request: Request,
    exc: InvalidTokenError | TokenExpiredError
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid or expired token."}
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials."}
    )


async def user_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User with this email already exists."}
    )
    

async def username_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Username already exists."}
    )    