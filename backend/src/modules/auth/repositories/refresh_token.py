from redis.asyncio import Redis
from datetime import datetime


class RefreshTokenRepository:
    def __init__(self, client: Redis):
        self.client = client

    def _key(self, jwt_id: str):
        return f"refresh:{jwt_id}"

    async def save_token(self, jwt_id: str, user_id: str, exp: datetime) -> None:
        await self.client.set(
            self._key(jwt_id),
            user_id,
            exat=exp,
        )

    async def token_exists(self, jwt_id: str) -> bool:
        return bool(await self.client.exists(self._key(jwt_id)))

    async def delete_token(self, jwt_id: str) -> bool:
        deleted = await self.client.delete(self._key(jwt_id))
        return deleted > 0
