# Orchestrates user-related application use cases.
# This service belongs to the application layer of the Clean Architecture and
# coordinates validation, business rules, password hashing, and persistence
# without implementing database access itself. Infrastructure concerns are
# provided through injected dependencies such as UserRepository and PasswordHasher.

from backend.src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserCreateInternal,
)
from backend.src.modules.user.models.user_model import UserModel
from backend.src.modules.user.repositories.user_repository import UserRepository
from backend.src.core.exceptions.user import (
    UserAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from backend.src.shared.interfaces.password_hasher import PasswordHasher


class UserService:
    """Coordinates application-level use cases related to users.

    The service acts as the application-layer boundary between incoming user
    data and the persistence layer. It is responsible for enforcing
    user-registration rules and coordinating password hashing and repository
    operations through injected dependencies.
    """

    def __init__(
        self,
        *,
        repo: UserRepository,
        password_hasher: PasswordHasher
    ):
        """Initialize the service with its persistence and password-hashing dependencies."""

        self.repo = repo
        self.password_hasher = password_hasher

    def create_internal_user(self, user_in: UserSignUp) -> UserCreateInternal:
        """Convert validated signup data into an internal user representation.

        The plain-text password is hashed before the data is passed toward the
        persistence layer, ensuring that the original password is never stored
        as part of the database creation flow.
        """

        hashed_password = self.password_hasher.hash_password(user_in.password)

        return UserCreateInternal(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password
        )

    async def register_user(self, *, user_in: UserSignUp) -> UserModel:
        """Register a new user after enforcing uniqueness and credential rules.

        The use case checks for existing email and username values, transforms
        the validated signup data into an internal representation, and delegates
        persistence to the repository.
        """

        user_in_db = await self.repo.get_user_by_email(email=user_in.email)

        if user_in_db:
            raise UserAlreadyExistsError()

        user_in_db = await self.repo.get_user_by_username(username=user_in.username)

        if user_in_db:
            raise UsernameAlreadyExistsError()

        internal_user = self.create_internal_user(user_in)
        user = await self.repo.create_user(internal_user=internal_user)

        return user