from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class BaseTokenPayload(BaseModel):
    sub: str
    exp: datetime | None = None
    type: str = ""

    def model_dump_payload(self, expires_delta: timedelta):
        self.exp = datetime.now(timezone.utc) + expires_delta
        return self.model_dump()


class AccessTokenPayload(BaseTokenPayload):
    type: str = Field("access", pattern=r"^access$")


class RefreshTokenPayload(BaseTokenPayload):
    type: str = Field("refresh", pattern=r"^refresh$")


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
