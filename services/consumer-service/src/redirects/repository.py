from clickhouse_connect.driver.client import Client
import pandas as pd

from src.redirects.schemas import RedirectSchema


class RedirectsRepository:
    def __init__(self, client: Client):
        self.client = client

    def store_redirects(self, redirects: list[RedirectSchema]):
        df = pd.DataFrame([redirect.model_dump() for redirect in redirects])
        self.client.insert_df("redirect_stats", df)
