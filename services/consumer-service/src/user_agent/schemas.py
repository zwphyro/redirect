from pydantic import BaseModel, Field


class UserAgentSchema(BaseModel):
    browser: str | None = Field(None)
    browser_version: str | None = Field(None)
    os: str | None = Field(None)
    os_version: str | None = Field(None)
    device: str | None = Field(None)
    device_brand: str | None = Field(None)
    device_model: str | None = Field(None)
    language: str | None = Field(None)
