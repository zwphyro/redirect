import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ch_db_name: str = Field(..., alias="CLICKHOUSE_DB")
    ch_host: str = Field(..., alias="CLICKHOUSE_HOST")
    ch_port: int = Field(..., alias="CLICKHOUSE_PORT")
    ch_user: str = Field(..., alias="CLICKHOUSE_USER")
    ch_password: str = Field(..., alias="CLICKHOUSE_PASSWORD")

    rabbitmq_host: str = Field(..., alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(..., alias="RABBITMQ_PORT")
    rabbitmq_user: str = Field(..., alias="RABBITMQ_DEFAULT_USER")
    rabbitmq_password: str = Field(..., alias="RABBITMQ_DEFAULT_PASS")

    @property
    def broker_url(self):
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}//"

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", ".env"
        ),
        extra="ignore",
    )


settings = Settings()  # type: ignore
