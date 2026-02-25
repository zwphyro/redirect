import requests

from src.ip_locator.schemas import IPLocationSchema


class IPLocator:
    # TODO: cache
    @classmethod
    def localte(cls, ip: str):
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=2147030")
        data = response.json()

        if data["status"] == "fail":
            return None

        return IPLocationSchema.model_validate(data)
