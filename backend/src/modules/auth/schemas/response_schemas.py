from pydantic import BaseModel


class LoginResponse(BaseModel):
    message: str