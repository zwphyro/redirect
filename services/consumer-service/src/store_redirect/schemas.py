from datetime import date, datetime
from pydantic import BaseModel

from src.ip.schemas import IPDataSchema
from src.user_agent.schemas import UserAgentSchema


class BaseRedirectSchema(BaseModel):
    time: datetime
    short_code: str
    ip: str
    user_agent: str
    language: str
    origin: str


class CompleteRedirectSchema(BaseModel):
    event_date: date
    event_time: datetime

    short_code: str

    ip: str
    continent_code: str
    country_code: str
    region_code: str
    city: str
    provider: str
    lat: float
    lon: float

    browser: str
    browser_version: str
    os: str
    os_version: str
    device: str
    device_brand: str
    device_model: str

    language: str

    origin: str

    @classmethod
    def from_base_models(cls, base_model: BaseRedirectSchema, ip_info: IPDataSchema, user_agent: UserAgentSchema):
        return cls(
            event_date=base_model.time.date(),
            event_time=base_model.time,
            short_code=base_model.short_code,
            ip=base_model.ip,
            continent_code=ip_info.continent_code,
            country_code=ip_info.country_code,
            region_code=ip_info.region_code,
            city=ip_info.city,
            provider=ip_info.provider,
            lat=ip_info.lat,
            lon=ip_info.lon,
            browser=user_agent.browser,
            browser_version=user_agent.browser_version,
            os=user_agent.os,
            os_version=user_agent.os_version,
            device=user_agent.device,
            device_brand=user_agent.device_brand,
            device_model=user_agent.device_model,
            language=user_agent.language,
            origin=base_model.origin,
        )
