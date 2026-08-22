# Defines the dependency providers used by the user and authentication
# modules.

# This module is responsible for constructing and wiring application
# dependencies for FastAPI. It keeps dependency creation out of routers and
# application services, while allowing concrete infrastructure implementations
# to be injected where an abstraction is expected.

from backend.src.modules.user.repositories.user_repository import UserRepository
from backend.src.modules.user.application.user_service import UserService
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.shared.interfaces.password_hasher import PasswordHasher
from backend.src.modules.auth.security.password import BcryptHasher
from backend.src.modules.auth.security.jwt import TokenManager
from backend.src.core.exceptions.token import InvalidTokenError
from backend.src.core.exceptions.user import UserNotFoundError
from backend.src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def get_user_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_db)
    ]
) -> UserRepository:
    """Create a user repository using the current database session.

    This dependency centralizes repository construction and allows FastAPI to
    provide the request-scoped database session to the persistence layer.
    """

    repo = UserRepository(db)
    return repo


def get_password_hasher() -> PasswordHasher:
    """Provide the concrete password-hashing implementation.

    The dependency returns the password hasher through its interface type,
    allowing application services to remain independent of the concrete
    hashing implementation.
    """

    password_hasher = BcryptHasher()
    return password_hasher


def get_token_manager() -> TokenManager:
    """Provide the token-management implementation used by authentication flows."""

    token_manager = TokenManager()
    return token_manager


def get_user_service(
    repo: Annotated[
        UserRepository,
        Depends(get_user_repository)
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher)
    ]
) -> UserService:
    """Construct the user application service with its required dependencies.

    Dependency construction is kept outside the service itself so the
    application layer does not need to know how its collaborators are created.
    """

    user_service = UserService(
        repo=repo,
        password_hasher=password_hasher
    )

    return user_service


def get_auth_service(
    user_repo: Annotated[
        UserRepository,
        Depends(get_user_repository)
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher)
    ],
    token_manager: Annotated[
        TokenManager,
        Depends(get_token_manager)
    ]
) -> AuthService:
    """Construct the authentication service with its required dependencies.

    This dependency wires together persistence, password verification, and
    token management while keeping the construction logic outside the
    authentication application service.
    """

    auth_service = AuthService(
        user_repo=user_repo,
        password_hasher=password_hasher,
        token_manager=token_manager
    )

    return auth_service


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security)
    ],
    token_manager: Annotated[
        TokenManager,
        Depends(get_token_manager)
    ],
    user_repo: Annotated[
        UserRepository,
        Depends(get_user_repository)
    ]
):
    """Resolve and return the authenticated user from the request token.

    The dependency validates the access token, extracts the user identifier,
    and retrieves the corresponding user from the repository. It is intended
    for protected endpoints that require an authenticated user.
    """

    payload = await token_manager.decode_access_token(
        credentials.credentials
    )

    user_id = payload.get("user_id")

    if not user_id:
        raise InvalidTokenError()

    user = await user_repo.get_user_by_id(user_id)

    if not user:
        raise UserNotFoundError()

    return user
