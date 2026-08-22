# Defines the base exception hierarchy used across the application.
#
# These exception types provide categories for application-level errors,
# allowing specific exceptions to inherit from a meaningful base type while
# keeping error handling independent from framework-specific exceptions.


class ServiceError(Exception):
    """Base exception for errors raised by application services."""

    pass


class TokenError(Exception):
    """Base exception for authentication and token-related errors."""

    pass


class GlobalError(Exception):
    """Base exception for application-wide errors not tied to a specific module."""

    pass