from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RedirectLinkSchema(BaseModel):
    id: int
    short_code: str
    target_url: str
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateRedirectLinkSchema(BaseModel):
    target_url: str
