from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from datetime import datetime
from backend.src.core.exceptions.redis_exc import RedisUnavailableError


class RefreshTokenRepository:
    
    """Manage refresh token state using Redis.

    Refresh tokens are stored by their JWT ID (jti), allowing the
    application to validate, rotate, and revoke refresh tokens
    independently of JWT signature validation.
    """
    
    def __init__(self, client: Redis):
        self.client = client

    def _key(self, jwt_id: str):
        return f"refresh:{jwt_id}"

    async def save_token(self, *, jwt_id: str, user_id: str, exp: datetime) -> None:
        try:
            await self.client.set(
                self._key(jwt_id),
                user_id,
                exat=exp,
            )
        except ConnectionError as exc:
            raise RedisUnavailableError() from exc

    async def token_exists(self, jwt_id: str) -> bool:
        try:
            return bool(await self.client.exists(self._key(jwt_id)))
        except ConnectionError as exc:
            raise RedisUnavailableError() from exc

    async def delete_token(self, jwt_id: str) -> bool:
        try:
            deleted = await self.client.delete(self._key(jwt_id))
        except ConnectionError as exc:
            raise RedisUnavailableError() from exc
        return deleted > 0
