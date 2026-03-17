import requests
from requests import RequestException, Response, Session

from src.ip.schemas import IPDataSchema
from src.settings import settings


class IPService:
    def __init__(self, *, session: Session | None = None):
        self._session = session or requests.Session()
        self._host = settings.ip_api_host.rstrip("/")
        self._timeout = settings.ip_api_timeout_seconds
        self._max_retries = settings.ip_api_max_retries

    def _request(self, ip: str) -> Response | None:
        url = f"{self._host}/json/{ip}?fields=2097878"

        for _ in range(self._max_retries):
            try:
                response = self._session.get(url, timeout=self._timeout)
            except RequestException:
                continue

            if response.status_code == 200:
                return response

        return None

    def get_ip_info(self, ip: str) -> IPDataSchema:
        response = self._request(ip)

        if response is None:
            return IPDataSchema.model_validate({})

        try:
            payload = response.json()
        except ValueError:
            return IPDataSchema.model_validate({})

        return IPDataSchema.model_validate(payload)
