from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend.src.modules.auth.schemas.login import LoginSchema
from backend.src.modules.auth.schemas.response_schemas import LoginResponse
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.modules.user.models.user_model import UserModel
from backend.src.shared.dependencies.user import get_auth_service, get_current_user
from backend.src.core.exceptions.user import InvalidCredentialsError, UserNotFoundError
from backend.src.core.exceptions.token import InvalidTokenError, TokenExpiredError

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    data: LoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    access_token, refresh_token = await service.login(email=data.email, password=data.password)
    # temporary response-this is obviously not safe:)
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
    


@router.get("/test-auth")
async def test_auth(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
        return {
            "message": "It works!",
            "user_id": str(current_user.id)
        }