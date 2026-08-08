from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend.src.modules.auth.schemas.login import LoginSchema
from backend.src.modules.auth.schemas.response_schemas import LoginResponse
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.shared.dependencies.user_dependencies import get_auth_service
from backend.src.core.exceptions.user import InvalidCredentialsError

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    data: LoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        access_token, refresh_token = await service.login(email=data.email, password=data.password)
        # temporary response-this is obviously not safe:)
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
