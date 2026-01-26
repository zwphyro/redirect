from datetime import datetime
from pydantic import BaseModel


class RedirectURLSchema(BaseModel):
    id: int
    short_code: str
    original_url: str
    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateRedirectURLSchema(BaseModel):
    original_url: str
