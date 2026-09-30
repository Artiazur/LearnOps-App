import os
from uuid import uuid4
from pytest_asyncio import fixture
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from unittest.mock import AsyncMock, Mock
from sqlalchemy.ext.asyncio import create_async_engine
from backend.src.shared.database.base import Base
from backend.src.modules.user.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from backend.src.modules.user.repositories.user_repository import UserRepository
from backend.src.modules.user.application.user_service import UserService


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env.test")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not configured")

test_engine = create_async_engine(
    url=TEST_DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@fixture(autouse=True)
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session


@fixture
async def test_repo(db_session):
    repo = UserRepository(db=db_session)
    return repo


@fixture
async def test_service(test_repo):
    return UserService(
        repo=test_repo,
        password_hasher=Mock()
    )


@fixture
async def persisted_user(db_session):
    user = UserModel(
        id=uuid4(),
        first_name="test",
        last_name="user",
        username="test_user",
        email="test.user@example.com",
        hashed_password="fake_hash",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user