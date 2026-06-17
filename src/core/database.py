from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from src.core.config import settings


engine = create_async_engine(
    settings.async_database_url,
    echo=True,
    pool_pre_ping=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
