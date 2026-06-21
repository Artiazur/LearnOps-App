from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserResponse
)
from src.modules.user.schemas.response_schemas import(
    RegisterResponse
)
from src.modules.user.application.user_service import UserService
from src.core.exceptions.user import (
    UserAlreadyExistsError,
    UsernameAlreadyExistsError
)
from src.shared.dependencies.dependencies import get_user_service


router = APIRouter(prefix="/users")


@router.post("/register",
             status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserSignUp,
    service: Annotated[UserService, Depends(get_user_service)]
) -> RegisterResponse:
    try:
        user = await service.register_user(user_in=user_in)
        return RegisterResponse(
            message="You registered successfully",
            user=UserResponse.model_validate(user)
        )

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )


