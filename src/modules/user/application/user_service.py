from src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserCreateInternal,
    UserUpdate
)
from src.modules.user.models.user_model import UserModel
from src.modules.user.repositories.user_repository import UserRepository
from src.core.exceptions.user import(
    UserAlreadyExistsError,
    UsernameAlreadyExistsError,
    UserNotFoundError
)
from src.core.security import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_internal_user(self, user_in: UserSignUp) -> UserCreateInternal:
        user_in.password = hash_password(user_in.password)
        return UserCreateInternal(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            username=user_in.username,
            email=user_in.email,
            password=user_in.password
        )

    async def register_user(self, *, user_in: UserSignUp) -> UserModel:
        internal_user = self.create_internal_user(user_in)
        user_in_db = await self.repo.get_user_by_email(email=internal_user.email)
        if user_in_db:
            raise UserAlreadyExistsError()
        user_in_db = await self.repo.get_user_by_username(username=internal_user.username)
        if user_in_db:
            raise UsernameAlreadyExistsError()
        user = await self.repo.create_user(internal_user=internal_user)
        return user
          
