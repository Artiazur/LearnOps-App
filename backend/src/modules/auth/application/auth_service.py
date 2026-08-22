# Coordinates the user authentication use case.
# This service belongs to the application layer and is responsible for
# validating credentials and orchestrating the authentication flow.
#
# Authentication-specific implementations such as password hashing and JWT
# handling are injected as dependencies, keeping the authentication workflow
# separate from the underlying security libraries and persistence operations.

from pydantic import EmailStr
from backend.src.core.exceptions.user import InvalidCredentialsError
from backend.src.shared.interfaces.password_hasher import PasswordHasher
from backend.src.modules.auth.security.jwt import TokenManager
from backend.src.modules.user.repositories.user_repository import UserRepository


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
        token_manager: TokenManager
    ):
        """Initialize the authentication service with its required dependencies."""

        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_manager = token_manager

    async def login(self, email: EmailStr, password: str):
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
        refresh_token = self.token_manager.create_refresh_token(data)

        return access_token, refresh_token