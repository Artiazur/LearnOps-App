from pydantic import EmailStr
from src.core.exceptions.user import InvalidCredentialsError
from src.modules.auth.security.password import PasswordHasher
from src.modules.user.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self,
                 *,
                 user_repo: UserRepository,
                 password_hasher: PasswordHasher
                 ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def login(self, email: EmailStr, password: str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsError()

        is_password_valid = self.password_hasher.verify_password(
            raw_password=password,
            hashed_password=user.hashed_password
        )
        if not is_password_valid:
            raise InvalidCredentialsError()
