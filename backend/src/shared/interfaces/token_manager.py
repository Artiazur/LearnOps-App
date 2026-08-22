# Defines the abstraction for token management used by the authentication
# layer.
#
# The application depends on this contract rather than on a specific token
# technology or implementation. Concrete implementations, such as
# JWTTokenManager, are responsible for providing the actual token operations.
#
# Keeping token management behind an abstraction allows the underlying
# authentication mechanism to be replaced without changing the application
# services or their consumers.

from abc import ABC, abstractmethod


class TokenManager(ABC):
    """Defines the contract for creating and validating authentication tokens.

    This abstraction separates token-related application behavior from the
    concrete token implementation. Authentication services and dependencies
    can therefore depend on the contract while the actual implementation is
    provided through dependency injection.
    """

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """Create an access token containing the supplied authentication data."""

        pass

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        """Create a refresh token containing the supplied authentication data."""

        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode and validate a token and return its payload."""

        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> dict:
        """Decode a token and ensure that it is an access token."""

        pass

    @abstractmethod
    def decode_refresh_token(self, token: str) -> dict:
        """Decode a token and ensure that it is a refresh token."""

        pass