# Defines the abstraction for password hashing operations.
#
# This interface belongs to the shared abstraction layer and establishes the
# contract required by the application layer without depending on a specific
# hashing library or algorithm. Concrete implementations, such as bcrypt,
# provide the actual password-hashing behavior.

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Defines the contract for password hashing and verification.

    Application services depend on this abstraction rather than directly on a
    concrete hashing implementation. This keeps authentication logic
    independent from the underlying password-hashing library and allows the
    implementation to be replaced without changing the application layer.
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain-text password for secure persistent storage."""

        pass

    @abstractmethod
    def verify_password(
        self,
        *,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        """Verify a plain-text password against its stored hash."""

        pass