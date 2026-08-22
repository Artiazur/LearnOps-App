# Provides JWT creation and validation for the authentication module.
# This component encapsulates token-related security operations, including
# signing, decoding, expiration handling, and token-type validation.
#
# Keeping JWT implementation details inside this component allows the
# application layer to depend on an authentication abstraction rather than
# directly interacting with the underlying JWT library.

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError, ExpiredSignatureError

from backend.src.core.config import settings, PRIVATE_KEY, PUBLIC_KEY

from backend.src.core.exceptions.token import InvalidTokenError, TokenExpiredError


class TokenManager:
    """Manages the creation and validation of JWT authentication tokens.

    The manager centralizes JWT-specific security logic so other parts of the
    authentication flow do not need to know how tokens are signed, decoded,
    expired, or distinguished by type.
    """

    async def create_access_token(self, data: dict):
        """Create a short-lived JWT used to authenticate API requests.

        The supplied claims are signed with the configured private key and
        marked as an access token so it can later be distinguished from a
        refresh token during validation.
        """

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})

        encoded_token = jwt.encode(
            to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_token

    async def create_refresh_token(self, data: dict):
        """Create a long-lived JWT used to obtain new access tokens.

        Refresh tokens use their own expiration policy and are explicitly
        marked as refresh tokens to prevent them from being accepted where
        an access token is required.
        """

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_token = jwt.encode(
            to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_token

    async def decode_token(self, token: str):
        """Decode and validate the signature and expiration of a JWT.

        This method provides the shared low-level token validation used by
        access and refresh token decoders. JWT library errors are translated
        into application-specific exceptions so higher layers remain
        independent of the underlying JWT implementation.
        """

        try:
            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload

        except ExpiredSignatureError:
            raise TokenExpiredError()

        except JWTError:
            raise InvalidTokenError()

    async def decode_access_token(self, token: str):
        """Validate and decode a JWT specifically as an access token.

        In addition to cryptographic and expiration validation, this method
        verifies that the token was issued for access-token usage.
        """

        payload = await self.decode_token(token)

        if payload.get("type") != "access":
            raise InvalidTokenError()

        return payload

    async def decode_refresh_token(self, token: str):
        """Validate and decode a JWT specifically as a refresh token.

        The token must pass the common JWT validation and contain the refresh
        token type claim before it can be used by the refresh-token flow.
        """

        payload = await self.decode_token(token)

        if payload.get("type") != "refresh":
            raise InvalidTokenError()

        return payload