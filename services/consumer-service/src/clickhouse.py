from src.settings import settings
from clickhouse_connect import get_client

client = get_client(
    host=settings.ch_host,
    port=settings.ch_port,
    username=settings.ch_user,
    password=settings.ch_password,
    database=settings.ch_db_name,
)
