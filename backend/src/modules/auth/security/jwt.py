from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from backend.src.core.config import settings, PRIVATE_KEY, PUBLIC_KEY
from backend.src.core.exceptions.token import InvalidTokenError, TokenExpiredError


class TokenManager:
    async def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_token = jwt.encode(
            to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
        return encoded_token

    async def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_token = jwt.encode(
            to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
        return encoded_token

    async def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[
                                 settings.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except JWTError:
            raise InvalidTokenError()

    async def decode_access_token(self, token: str):
        payload = await self.decode_token(token)

        if payload.get("type") != "access":
            raise InvalidTokenError()

        return payload
    
    async def decode_refresh_token(self, token: str):
        payload = await self.decode_token(token)
    
        if payload.get("type") != "refresh":
            raise InvalidTokenError()
    
        return payload