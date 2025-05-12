import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_DIR = Path(__file__).resolve().parent.parent
_ENV_DIR = os.path.join(_BASE_DIR, '.env')


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_DIR,
        env_file_encoding='utf-8',
        env_prefix="POSTGRES_",
        extra="ignore",
    )
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def db_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def db_url_sync(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Config(BaseSettings):
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


config = Config()
