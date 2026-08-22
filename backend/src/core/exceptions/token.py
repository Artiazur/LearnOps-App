# Defines authentication-related exceptions for invalid and expired tokens.
#
# These exceptions inherit from the shared TokenError category so token
# validation failures can be handled consistently by the application-level
# exception handling layer without coupling the authentication logic to
# FastAPI or another web framework.

from backend.src.core.exceptions.base import TokenError


class InvalidTokenError(TokenError):
    """Raised when a token is invalid or fails token validation."""

    pass


class TokenExpiredError(TokenError):
    """Raised when a token has expired and can no longer be accepted."""

    pass