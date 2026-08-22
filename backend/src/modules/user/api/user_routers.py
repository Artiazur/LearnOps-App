# Defines the HTTP endpoints for the user module.
# This module belongs to the presentation/API layer of the Clean Architecture.
# Its responsibility is limited to handling HTTP concerns, validating request
# data through Pydantic schemas, resolving application dependencies, and
# translating application results into API responses. Business logic remains
# inside the application layer.

from typing import Annotated
from fastapi import APIRouter, Depends, status
from backend.src.modules.user.schemas.user_schemas import (
    UserSignUp,
    UserResponse
)
from backend.src.modules.user.schemas.response_schemas import (
    RegisterResponse
)
from backend.src.modules.user.application.user_service import UserService
from backend.src.shared.dependencies.user import get_user_service


router = APIRouter(prefix="/users")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_in: UserSignUp,
    service: Annotated[UserService, Depends(get_user_service)]
) -> RegisterResponse:
    """Register a new user through the user application service.

    The endpoint acts as the presentation-layer entry point for registration.
    It delegates the registration use case to UserService and converts the
    resulting persistence model into the public UserResponse schema before
    returning the API response.

    Keeping the endpoint focused on HTTP and data-contract concerns prevents
    application logic from leaking into the API layer.
    """

    user = await service.register_user(user_in=user_in)

    return RegisterResponse(
        message="You registered successfully",
        user=UserResponse.model_validate(user)
    )
