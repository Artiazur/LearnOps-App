# Centralizes application configuration and environment-based settings.
#
# This module provides a single configuration source for database access,
# authentication, and cryptographic key locations. Keeping configuration in
# one place prevents infrastructure details from being scattered throughout
# the application and allows environment-specific values to be supplied
# without changing application code.

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Represents the application's environment-driven configuration.

    Pydantic Settings loads and validates configuration values from the
    environment and the project's ``.env`` file, providing typed access to
    infrastructure and authentication settings throughout the application.
    """

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    PRIVATE_KEY_PATH: str
    PUBLIC_KEY_PATH: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )

    @property
    def async_database_url(self) -> str:
        """Build the database URL used by the asynchronous SQLAlchemy engine.

        The URL uses the ``asyncpg`` PostgreSQL driver required for the
        application's asynchronous database operations.
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        """Build the database URL used by synchronous database operations.

        This provides a separate connection URL using the ``psycopg`` driver
        for tooling or application components that require synchronous
        database access.
        """

        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Create the application's validated configuration object once and reuse it
# wherever configuration values are required.
settings = Settings()


# Load the RSA keys once during application initialization so authentication
# components can use them without repeatedly reading the key files from disk.
PRIVATE_KEY = (
    BASE_DIR / settings.PRIVATE_KEY_PATH
).read_text()

PUBLIC_KEY = (
    BASE_DIR / settings.PUBLIC_KEY_PATH
).read_text()