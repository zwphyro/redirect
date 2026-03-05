from clickhouse_connect.driver.client import Client


class RedirectsRepository:
    def __init__(self, client: Client):
        self.client = client
