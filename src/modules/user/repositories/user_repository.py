from src.modules.user.models.user_model import UserTable
from src.modules.user.schemas.user_schemas import UserCreateInternal
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(*, internal_user: UserCreateInternal, db: AsyncSession):
    user_data = internal_user.model_dump()
    user = UserTable(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user