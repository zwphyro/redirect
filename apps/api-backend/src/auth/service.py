from datetime import datetime, timezone
from pwdlib import PasswordHash
from src.auth.exceptions import (
    IncorrectLoginOrPasswordError,
    InvalidPayloadError,
    TokenExpiredError,
    UserNotFoundError,
)
from src.auth.schemas import AccessTokenPayload, RefreshTokenPayload
from src.auth.token import Token
from src.unit_of_work import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork, password_hash: PasswordHash, token: Token):
        self._uow = uow
        self._password_hash = password_hash
        self._token = token

    async def register(self, email: str, password: str):
        user = await self._uow.auth.get_user_by_email(email)

        if user is not None:
            # INFO: explicitly ignore if user already exists
            return

        password_hash = self._password_hash.hash(password)

        try:
            await self._uow.auth.create_user(email, password_hash)
            await self._uow.commit()
        except Exception:
            await self._uow.rollback()

    async def login(self, email: str, password: str):
        user = await self._uow.auth.get_user_by_email(email)

        if user is None:
            raise IncorrectLoginOrPasswordError("Incorrect login or password")

        if not self._password_hash.verify(password, user.password_hash):
            raise IncorrectLoginOrPasswordError("Incorrect login or password")

        user_id = str(user.id)
        access_token = self._token.create_access_token(AccessTokenPayload(sub=user_id))
        refresh_token = self._token.create_refresh_token(
            RefreshTokenPayload(sub=user_id)
        )

        return access_token, refresh_token

    async def get_current_user(self, access_token: str):
        payload = self._token.decode_access_token(access_token)

        if payload is None:
            raise InvalidPayloadError("Can't decode access token")

        if payload.exp is None or payload.exp < datetime.now(timezone.utc):
            raise TokenExpiredError("Token expired")

        user_id = payload.sub
        user = await self._uow.auth.get_user_by_id(int(user_id))

        if user is None:
            raise UserNotFoundError("User not found")

        return user

    async def refresh(self, refresh_token: str):
        payload = self._token.decode_refresh_token(refresh_token)

        if payload is None:
            raise InvalidPayloadError("Can't decode access token")

        if payload.exp is None or payload.exp < datetime.now(timezone.utc):
            raise TokenExpiredError("Token expired")

        user_id = payload.sub
        user = await self._uow.auth.get_user_by_id(int(user_id))

        if user is None:
            raise UserNotFoundError("User not found")

        user_id = str(user.id)
        access_token = self._token.create_access_token(AccessTokenPayload(sub=user_id))
        new_refresh_token = self._token.create_refresh_token(
            RefreshTokenPayload(sub=user_id)
        )

        return access_token, new_refresh_token
