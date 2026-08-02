from pydantic import BaseModel
from backend.src.modules.user.schemas.user_schemas import UserResponse

class RegisterResponse(BaseModel):
    message: str
    user: UserResponse