from src.modules.user.models.user_model import UserModel
from src.modules.user.schemas.user_schemas import UserCreateInternal
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    update,
    delete,
    func
)


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, *, internal_user: UserCreateInternal) -> UserModel:
        try:
            user_data = internal_user.model_dump()
            user = UserModel(**user_data)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception:
            raise

    async def get_user_by_email(self, email: EmailStr) -> UserModel | None:
        statement = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.username == username)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
