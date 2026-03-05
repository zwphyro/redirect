from pydantic import BaseModel, Field


class IPDataSchema(BaseModel):
    continent_code: str = Field(alias="continentCode")
    country_code: str = Field(alias="countryCode")
    region_code: str = Field(alias="region")
    city: str
    provider: str = Field(alias="isp")
    lat: float
    lon: float
