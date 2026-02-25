import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ch_name: str = Field(..., alias="CLICKHOUSE_DB")
    ch_host: str = Field(..., alias="CLICKHOUSE_HOST")
    ch_port: int = Field(..., alias="CLICKHOUSE_PORT")
    ch_user: str = Field(..., alias="CLICKHOUSE_USER")
    ch_password: str = Field(..., alias="CLICKHOUSE_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", ".env"
        ),
        extra="ignore",
    )


settings = Settings()  # type: ignore
