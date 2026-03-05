from settings import settings
from clickhouse_connect import get_client

client = get_client(
    host=settings.ch_host,
    port=settings.ch_port,
    database=settings.ch_name,
    username=settings.ch_user,
    password=settings.ch_password,
)
