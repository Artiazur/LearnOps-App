# Configures the application's asynchronous SQLAlchemy database connection.
#
# This module centralizes database engine and session management so application
# components can obtain database sessions without handling connection
# lifecycle details themselves. The dependency-based session provider also
# allows FastAPI to manage a session for each request that requires database
# access.

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from backend.src.core.config import settings


# Create the shared asynchronous database engine using the configured
# PostgreSQL connection URL.
engine = create_async_engine(
    settings.async_database_url,
    echo=True,
    pool_pre_ping=True
)


# Session factory used to create asynchronous SQLAlchemy sessions.
# Disabling expiration on commit keeps loaded attributes available after a
# transaction is committed.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """Provide a database session for the duration of a request.

    The session is yielded to the consumer and always closed afterward,
    ensuring that database resources are released even when the request
    raises an exception.
    """

    session = AsyncSessionLocal()

    try:
        yield session
    finally:
        await session.close()