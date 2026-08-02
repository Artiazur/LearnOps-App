from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from backend.src.core.config import settings, PRIVATE_KEY, PUBLIC_KEY
from backend.src.core.exceptions.token import InvalidTokenError, TokenExpiredError


class TokenCreator:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_token = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
        return encoded_token
    
    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_token = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
        return encoded_token, expire

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except JWTError:
            raise InvalidTokenError()