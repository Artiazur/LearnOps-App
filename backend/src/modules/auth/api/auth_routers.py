from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend.src.modules.auth.schemas.login import LoginSchema
from backend.src.modules.auth.schemas.response_schemas import LoginResponse
from backend.src.modules.auth.application.auth_service import AuthService
from backend.src.shared.dependencies.dependencies import get_auth_service
from backend.src.core.exceptions.user import InvalidCredentialsError

90
router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    data: LoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        await service.login(email=data.email, password=data.password)
        return LoginResponse(message="You logged in successfully")     #temporary response-it will be replaced with tokens
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
