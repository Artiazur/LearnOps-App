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
    UserResponse,
    UserUpdate
)
from backend.src.modules.user.schemas.response_schemas import (
    RegisterResponse,
    UpdateResponse
)
from backend.src.modules.user.models.user_model import UserModel
from backend.src.modules.user.application.user_service import UserService
from backend.src.shared.dependencies.user import get_user_service, get_current_user


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


@router.get("/me", response_model=UserResponse)
async def show_user_profile(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UpdateResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[UserService, Depends(get_user_service)]
):
    updated_profile = await service.update_user_profile(
        user_update=user_update,
        user_id=current_user.id
    )
    
    profile_model = UserResponse.model_validate(updated_profile)
    return UpdateResponse(
        message="Your profile updated successfully.",
        user=profile_model
    )
