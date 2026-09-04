from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class RefreshTokenData(BaseModel):
    jti: str 
    user_id: str
    type: str 
    exp: datetime