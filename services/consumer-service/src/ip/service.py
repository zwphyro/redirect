import requests

from src.ip.schemas import IPDataSchema


class IPService:
    def __init__(self):
        pass

    def get_ip_info(self, ip: str):
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=2097878")

        if response.status_code != 200:
            return IPDataSchema.model_validate({})

        return IPDataSchema.model_validate(response.json())
