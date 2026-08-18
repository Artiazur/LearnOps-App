from backend.src.modules.user.repositories.user_repository import UserRepository
from backend.src.modules.user.application.user_service import UserService
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.shared.interfaces.password_hasher import PasswordHasher
from backend.src.modules.auth.security.password import BcryptHasher
from backend.src.modules.auth.security.jwt import TokenManager
from backend.src.core.exceptions.token import InvalidTokenError
from backend.src.core.exceptions.user import UserNotFoundError
from backend.src.core.exceptions.global_errors import SomethingWentWrong
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
        ]) -> UserRepository:
    repo = UserRepository(db)
    return repo


def get_password_hasher() -> PasswordHasher:
    password_hasher = BcryptHasher()
    return password_hasher


def get_token_manager() -> TokenManager:
    token_manager = TokenManager()
    return token_manager


def get_user_service(
        repo: Annotated[
            UserRepository,
            Depends(get_user_repository)],
        password_hasher: Annotated[
            PasswordHasher,
            Depends(get_password_hasher)]
) -> UserService:
    user_service = UserService(repo=repo, password_hasher=password_hasher)
    return user_service


def get_auth_service(
        user_repo: Annotated[
            UserRepository,
            Depends(get_user_repository)],
        password_hasher: Annotated[
            PasswordHasher,
            Depends(get_password_hasher)],
        token_manager: Annotated[
            TokenManager,
            Depends(get_token_manager)
        ]
) -> AuthService:
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
