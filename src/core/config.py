from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        
    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()