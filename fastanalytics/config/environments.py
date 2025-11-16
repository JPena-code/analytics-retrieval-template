from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".app.env",),
        env_file_encoding="utf-8",
        extra="allow",
    )

    pg_dsn: PostgresDsn
    debug: bool = False


Settings = _Settings()  # type: ignore
