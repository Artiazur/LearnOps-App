# Provides the data-access layer for the user module.
# The repository encapsulates SQLAlchemy-specific persistence logic so that
# application services can work with user data without depending directly
# on database queries. This separation follows the Repository pattern within
# the infrastructure/data-access side of Clean Architecture.

from backend.src.modules.user.models.user_model import UserModel
from backend.src.modules.user.schemas.user_schemas import UserCreateInternal
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    """Provides persistence operations for user entities.

    This repository acts as the boundary between the application and the
    database, encapsulating SQLAlchemy queries and session management for
    user-related data access.
    """

    def __init__(self, db: AsyncSession):
        """Initialize the repository with the database session used for persistence."""

        self.db = db

    async def create_user(self, *, internal_user: UserCreateInternal) -> UserModel:
        """Persist a new user using already-validated internal user data.

        The repository converts the application schema into a database model,
        persists it, and refreshes the instance so the caller receives the
        complete database entity, including generated fields such as its ID.
        """

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
        """Retrieve a user by email address.

        Used when the application needs to identify a user through their
        unique email, such as authentication or registration checks.
        """

        statement = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserModel | None:
        """Retrieve a user by username.

        Provides a dedicated persistence operation for use cases that need to
        locate a user through their username without exposing SQLAlchemy query
        details to higher application layers.
        """

        statement = select(UserModel).where(UserModel.username == username)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: str) -> UserModel | None:
        """Retrieve a user by their unique identifier.

        This operation provides the application layer with a simple way to
        resolve a persisted user entity from its ID while keeping the database
        query implementation inside the repository.
        """

        statement = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()