# Provides the concrete JWT-based implementation of the token management
# contract used by the authentication module.
#
# This component encapsulates JWT-specific security operations, including
# token creation, signature validation, expiration handling, and token-type
# validation.
#
# The application layer depends on the TokenManager abstraction rather than
# this concrete implementation. This keeps JWT-specific details isolated
# from authentication use cases and allows the token management mechanism
# to be replaced without changing the application layer.

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from backend.src.shared.interfaces.token_manager import TokenManager
from backend.src.core.config import settings, PRIVATE_KEY, PUBLIC_KEY
from backend.src.core.exceptions.token import (
    InvalidTokenError,
    TokenExpiredError
)


class JWTTokenManager(TokenManager):
    """Provides JWT-based token management for the authentication system.

    This class implements the TokenManager contract using JWT and the
    configured RSA keys. It is responsible for creating access and refresh
    tokens, decoding and validating tokens, and ensuring that a token is used
    for its intended purpose.

    JWT-specific implementation details remain isolated in the security layer,
    while application services interact with the TokenManager abstraction.
    """

    def create_access_token(self, data: dict):
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

    def create_refresh_token(self, data: dict):
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

    def decode_token(self, token: str):
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

    def decode_access_token(self, token: str):
        """Validate and decode a JWT specifically as an access token.

        In addition to cryptographic and expiration validation, this method
        verifies that the token was issued for access-token usage.
        """

        payload = self.decode_token(token)

        if payload.get("type") != "access":
            raise InvalidTokenError()

        return payload

    def decode_refresh_token(self, token: str):
        """Validate and decode a JWT specifically as a refresh token.

        The token must pass the common JWT validation and contain the refresh
        token type claim before it can be used by the refresh-token flow.
        """

        payload = self.decode_token(token)

        if payload.get("type") != "refresh":
            raise InvalidTokenError()

        return payload
