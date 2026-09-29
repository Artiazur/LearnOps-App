import pytest
from backend.src.modules.user.schemas.user_schemas import UserUpdate


@pytest.mark.asyncio
async def test_update_user_profile(
    user_service,
    fake_user,
    fake_repo
):
    data_for_update = {
        "first_name": "update_test_user",
        "phone_number": "4155551213"
    }
    user_update = UserUpdate.model_validate(data_for_update)
    result = await user_service.update_user_profile(
        user_update=user_update,
        user_id=fake_user.id
    )

    fake_repo.update_user.assert_awaited_once_with(
        update_data=data_for_update,
        user_id=fake_user.id
    )
    assert result == fake_user


@pytest.mark.asyncio
async def test_update_with_none(
    user_service,
    fake_user,
    fake_repo
):

    data_for_update = {
        "first_name": "update_test_user",
        "phone_number": "4155551213",
        "avatar_url": None
    }
    user_update = UserUpdate.model_validate(data_for_update)
    result = await user_service.update_user_profile(
        user_update=user_update,
        user_id=fake_user.id
    )
    fake_repo.update_user.assert_awaited_once_with(
        update_data=data_for_update,
        user_id=fake_user.id
    )
    assert result == fake_user
    
    
