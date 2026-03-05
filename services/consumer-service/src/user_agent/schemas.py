from pydantic import BaseModel


class UserAgentSchema(BaseModel):
    browser: str
    browser_version: str
    os: str
    os_version: str
    device: str
    device_brand: str
    device_model: str
    language: str
