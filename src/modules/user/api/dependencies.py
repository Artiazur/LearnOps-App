from src.modules.user.repositories.user_repository import UserRepository
from src.modules.user.application.user_service import UserService
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    repo = UserRepository(db)
    return repo


def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    service = UserService(repo)
    return service
