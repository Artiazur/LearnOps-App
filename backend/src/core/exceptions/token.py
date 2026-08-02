from backend.src.core.exceptions.base import TokenError


class InvalidTokenError(Exception):
    pass


class TokenExpiredError(Exception):
    pass