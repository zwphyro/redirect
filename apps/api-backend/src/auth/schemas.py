from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class BaseTokenPayload(BaseModel):
    sub: str
    exp: datetime | None = None

    def model_dump_payload(self, expires_delta: timedelta):
        self.exp = datetime.now(timezone.utc) + expires_delta
        return self.model_dump()


class AccessTokenPayload(BaseTokenPayload): ...


class RefreshTokenPayload(BaseTokenPayload): ...


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
