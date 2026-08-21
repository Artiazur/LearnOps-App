# Defines the SQLAlchemy persistence model for users.
# This model represents the database structure of the users table and belongs
# to the persistence/infrastructure side of the architecture. It is kept
# separate from the Pydantic schemas so database concerns do not leak into
# API or application-layer data contracts.

from backend.src.shared.database.base import Base
from backend.src.shared.mixins.repr_mixin import ReprMixin
from backend.src.shared.enum.user_roles import UserRole
from sqlalchemy import String, Date, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import date, datetime
import uuid


class UserModel(Base, ReprMixin):
    """SQLAlchemy model representing a persisted user.

    The model defines the database representation of a user, including
    identity, authentication data, profile information, account status,
    timestamps, and authorization role.

    It inherits from the shared database base for common ORM configuration
    and from ReprMixin for a consistent object representation across models.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    first_name: Mapped[str] = mapped_column(String(30), nullable=False)

    last_name: Mapped[str] = mapped_column(String(30), nullable=False)

    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            name="userrole",
            create_type=True
        ),
        default=UserRole.STUDENT,
        nullable=False
    )