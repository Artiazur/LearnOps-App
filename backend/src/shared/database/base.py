# Defines the base class inherited by all SQLAlchemy ORM models.
#
# Keeping the declarative base in the shared database layer allows all modules
# to use a common SQLAlchemy metadata registry and keeps ORM configuration
# independent from individual feature modules.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    SQLAlchemy models inherit from this class to participate in the declarative
    ORM system and share the application's database metadata.
    """

    pass
