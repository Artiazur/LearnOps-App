from src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserCreateInternal,
    UserUpdate
)
from src.modules.user.models.user_model import UserTable
from src.modules.user.repositories import user_repository
from sqlalchemy.ext.asyncio import AsyncSession


def create_internal_user(user_in: UserSignUp) -> UserCreateInternal:
    return UserCreateInternal(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password
    )


async def register_user(*, user: UserCreateInternal, db: AsyncSession) -> UserTable:
    return await user_repository.create_user(internal_user=user, db=db)
