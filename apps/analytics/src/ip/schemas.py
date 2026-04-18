from pydantic import BaseModel, Field


class IPDataSchema(BaseModel):
    continent_code: str | None = Field(None, alias="continentCode")
    country_code: str | None = Field(None, alias="countryCode")
    region_code: str | None = Field(None, alias="region")
    city: str | None = Field(None)
    provider: str | None = Field(None, alias="isp")
    lat: float | None = Field(None)
    lon: float | None = Field(None)
