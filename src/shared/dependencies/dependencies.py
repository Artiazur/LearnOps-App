from src.modules.user.repositories.user_repository import UserRepository
from src.modules.user.application.user_service import UserService
from src.modules.auth.application.auth_service import AuthService
from src.shared.interfaces.password_hasher import PasswordHasher
from src.modules.auth.security.password import BcryptHasher
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


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
            Depends(get_password_hasher)]
) -> AuthService:
    auth_service = AuthService(user_repo=user_repo, password_hasher=password_hasher)
    return auth_service
