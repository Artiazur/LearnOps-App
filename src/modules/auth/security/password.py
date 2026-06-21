from src.shared.interfaces.password_hasher import PasswordHasher
from passlib.context import CryptContext


class BcryptHasher(PasswordHasher):
    def __init__(self):
        self.password_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(
        self, *,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        return self.password_context.verify(raw_password, hashed_password)
