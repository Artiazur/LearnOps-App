from pydantic import BaseModel
from src.modules.user.schemas.user_schemas import UserResponse

class RegisterResponse(BaseModel):
    message: str
    user: UserResponse