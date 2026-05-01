from functools import lru_cache
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = Field(..., alias="POSTGRES_DB")
    db_host: str = Field(..., alias="POSTGRES_HOST")
    db_port: int = Field(..., alias="POSTGRES_PORT")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_password: str = Field(..., alias="POSTGRES_PASSWORD")

    host: str = Field(..., alias="BACKEND_HOST")
    port: int = Field(..., alias="BACKEND_PORT")
    jwt_algorithm: str = Field(..., alias="BACKEND_JWT_ALGORITHM")
    jwt_secret_key: str = Field(..., alias="BACKEND_JWT_SECRET_KEY")
    access_token_expire_minutes: int = Field(
        ..., alias="BACKEND_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(
        ..., alias="BACKEND_REFRESH_TOKEN_EXPIRE_DAYS"
    )

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", ".env"
        ),
        extra="ignore",
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings():
    return Settings()  # type: ignore
