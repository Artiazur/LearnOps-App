# Defines user-related application exceptions.
#
# These exceptions represent failures that can occur during user management
# and authentication use cases. They inherit from ServiceError so the
# application can categorize service-level failures independently from the
# HTTP layer.

from backend.src.core.exceptions.base import ServiceError


class UserAlreadyExistsError(ServiceError):
    """Raised when a user with the same email already exists."""

    pass


class UsernameAlreadyExistsError(ServiceError):
    """Raised when the requested username is already in use."""

    pass


class InvalidCredentialsError(ServiceError):
    """Raised when the provided authentication credentials are invalid."""

    pass


class UserNotFoundError(ServiceError):
    """Raised when the requested user cannot be found."""

    pass