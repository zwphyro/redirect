from clickhouse_connect.driver.client import Client
import pandas as pd

from src.redirect_events.schemas import RedirectEventSchema


class RedirectEventsRepository:
    def __init__(self, client: Client):
        self.client = client

    def store_redirect_events(self, redirect_events: list[RedirectEventSchema]):
        df = pd.DataFrame(
            [redirect_event.model_dump() for redirect_event in redirect_events]
        )
        self.client.insert_df("redirect_events", df)
