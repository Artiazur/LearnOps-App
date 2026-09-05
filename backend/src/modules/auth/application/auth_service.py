# Coordinates the user authentication use case.
# This service belongs to the application layer and is responsible for
# validating credentials and orchestrating the authentication flow.
#
# Authentication-specific implementations such as password hashing and JWT
# handling are injected as dependencies, keeping the authentication workflow
# separate from the underlying security libraries and persistence operations.

from pydantic import EmailStr
from backend.src.core.exceptions.user import (
    InvalidCredentialsError,
    UserNotFoundError
)
from backend.src.core.exceptions.token import InvalidTokenError, MissingRefreshTokenError
from backend.src.shared.interfaces.password_hasher import PasswordHasher
from backend.src.modules.auth.security.jwt import TokenManager
from backend.src.modules.user.repositories.user_repository import UserRepository
from backend.src.modules.auth.repositories.refresh_token import RefreshTokenRepository


class AuthService:
    """Coordinates the application-level user login flow.

    The service retrieves the user through the repository, verifies the
    supplied credentials through the password-hashing dependency, and issues
    authentication tokens after successful verification.

    External security and persistence concerns are delegated to injected
    dependencies so the authentication use case remains focused on its
    application-level responsibilities.
    """

    def __init__(
        self,
        *,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
        refresh_token_repo: RefreshTokenRepository
    ):
        """Initialize the authentication service with its required dependencies."""

        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_manager = token_manager
        self.refresh_token_repo = refresh_token_repo

    async def login(self, email: EmailStr, password: str) -> tuple[str, str]:
        """Authenticate a user and issue access and refresh tokens.

        The login flow first resolves the user by email, then verifies the
        supplied password against the stored password hash. If the credentials
        are valid, access and refresh tokens are generated for the user.

        Invalid email and password combinations intentionally result in the
        same application-level exception to avoid revealing whether a user
        account exists.
        """

        user = await self.user_repo.get_user_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        is_password_valid = self.password_hasher.verify_password(
            raw_password=password,
            hashed_password=user.hashed_password
        )

        if not is_password_valid:
            raise InvalidCredentialsError()

        data = {"user_id": str(user.id)}

        access_token = self.token_manager.create_access_token(data)
        refresh_token, refresh_data = self.token_manager.create_refresh_token(
            data)

        await self.refresh_token_repo.save_token(
            jwt_id=refresh_data.jti,
            user_id=refresh_data.user_id,
            exp=refresh_data.exp
        )

        return access_token, refresh_token

    async def logout(self, refresh_token: str):
        payload = self.token_manager.decode_refresh_token(refresh_token)
        jwt_id = payload["jti"]
        user_id = payload["user_id"]

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        deleted = await self.refresh_token_repo.delete_token(jwt_id)
        if not deleted:
            raise InvalidTokenError()

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        """Validate a refresh token and issue a new token pair.

        The refresh token is decoded and validated before resolving the associated
        user through the repository. A new access token and refresh token are then
        generated for the authenticated user.

        Token validation and user resolution are handled through the injected
        dependencies, keeping the refresh flow within the application layer while
        leaving HTTP-specific responsibilities to the API layer.
        """

        payload = self.token_manager.decode_refresh_token(refresh_token)
        jwt_id = payload["jti"]
        user_id = payload["user_id"]

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        deleted = await self.refresh_token_repo.delete_token(jwt_id)
        if not deleted:
            raise InvalidTokenError()

        new_access_token = self.token_manager.create_access_token(
            data={"user_id": user_id}
        )
        new_refresh_token, refresh_data = self.token_manager.create_refresh_token(
            data={"user_id": user_id}
        )
        await self.refresh_token_repo.save_token(
            jwt_id=refresh_data.jti,
            user_id=refresh_data.user_id,
            exp=refresh_data.exp
        )

        return new_access_token, new_refresh_token
