from clickhouse_connect import get_client
from clickhouse_connect.driver.client import Client

from src.settings import settings

_client: Client | None = None


def get_clickhouse_client() -> Client:
    global _client

    if _client is None:
        _client = get_client(
            host=settings.ch_host,
            port=settings.ch_port,
            username=settings.ch_user,
            password=settings.ch_password,
            database=settings.ch_db_name,
        )

    return _client
