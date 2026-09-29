from pytest import fixture
from uuid import uuid4
from unittest.mock import AsyncMock, Mock
from backend.src.modules.user.models.user_model import UserModel
from backend.src.modules.user.application.user_service import UserService


@fixture
def fake_password_hasher() -> Mock:
    fake_password_hasher = Mock()
    return fake_password_hasher


@fixture
def fake_user() -> UserModel:
    user = UserModel(
        id=uuid4(),
        first_name="test_user",
        last_name="1",
        username="update_user",
        email="testuser1@gmail.com",
        hashed_password="skgfkwegffbkjw"
    )
    return user


@fixture
def fake_repo(fake_user):
    repo = AsyncMock()
    repo.update_user.return_value = fake_user
    return repo


@fixture
def user_service(
    fake_repo,
    fake_password_hasher
):
    fake_service = UserService(
        repo=fake_repo,
        password_hasher=fake_password_hasher
    )
    return fake_service
