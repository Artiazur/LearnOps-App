import pytest
from backend.src.modules.user.schemas.user_schemas import UserUpdate
from backend.src.core.exceptions.user import NonNullableFieldError



@pytest.mark.asyncio
async def test_update_non_nullable(
    test_service,
    persisted_user
):
    data_for_update = {
        "first_name": None,
        "phone_number": "099999999999"
    }

    user_update = UserUpdate.model_validate(data_for_update)
    with pytest.raises(NonNullableFieldError):
        await test_service.update_user_profile(
            user_update=user_update,
            user_id=persisted_user.id,
        )
