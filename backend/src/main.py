from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.modules.user.api.user_routers import router as user_router
from backend.src.modules.auth.api.auth_routers import router as auth_router
from backend.src.core.exceptions.token import (
    InvalidTokenError,
    TokenExpiredError
)
from backend.src.core.exceptions.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UsernameAlreadyExistsError
)
from backend.src.shared.handlers import(
    token_error_handler,
    invalid_credentials_handler,
    user_exists_handler,
    username_exists_handler
)


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    InvalidTokenError,
    token_error_handler
)

app.add_exception_handler(
    TokenExpiredError,
    token_error_handler
)

app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler
)

app.add_exception_handler(
    UserAlreadyExistsError,
    user_exists_handler
)

app.add_exception_handler(
    UsernameAlreadyExistsError,
    username_exists_handler
)