
# Provides the concrete password-hashing implementation used by the
# authentication module.
# The authentication layer depends on the PasswordHasher abstraction rather
# than directly on Passlib, allowing the hashing implementation to be replaced
# without changing application-layer authentication logic.

from backend.src.shared.interfaces.password_hasher import PasswordHasher
from passlib.context import CryptContext


class BcryptHasher(PasswordHasher):
    """Hashes and verifies passwords using the bcrypt algorithm.

    This class implements the PasswordHasher abstraction and encapsulates
    Passlib-specific configuration and operations within the security layer.
    """

    def __init__(self):
        """Initialize the password hashing context with the bcrypt scheme."""

        self.password_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    def hash_password(self, password: str) -> str:
        """Create a secure hash from a plain-text password.

        The resulting hash is intended for persistent storage instead of the
        original password.
        """

        return self.password_context.hash(password)

    def verify_password(
        self, *,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        """Verify a plain-text password against its stored hash.

        Returns whether the provided credentials match without exposing the
        underlying password-hashing implementation to the application layer.
        """

        return self.password_context.verify(raw_password, hashed_password)
