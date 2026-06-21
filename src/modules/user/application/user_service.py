from src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserCreateInternal,
    UserUpdate
)
from src.modules.user.models.user_model import UserModel
from src.modules.user.repositories.user_repository import UserRepository
from src.core.exceptions.user import (
    UserAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from src.shared.interfaces.password_hasher import PasswordHasher


class UserService:
    def __init__(
        self,
        *,
        repo: UserRepository,
        password_hasher: PasswordHasher
    ):
        self.repo = repo
        self.password_hasher = password_hasher

    def create_internal_user(self, user_in: UserSignUp) -> UserCreateInternal:
        hashed_password = self.password_hasher.hash_password(user_in.password)
        return UserCreateInternal(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password
        )

    async def register_user(self, *, user_in: UserSignUp) -> UserModel:
        user_in_db = await self.repo.get_user_by_email(email=user_in.email)
        if user_in_db:
            raise UserAlreadyExistsError()
        user_in_db = await self.repo.get_user_by_username(username=user_in.username)
        if user_in_db:
            raise UsernameAlreadyExistsError()
        internal_user = self.create_internal_user(user_in)

        user = await self.repo.create_user(internal_user=internal_user)
        return user
