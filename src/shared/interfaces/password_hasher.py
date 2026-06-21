from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(password: str) -> str:
        pass

    @abstractmethod
    def verify_password(
        *,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        pass
