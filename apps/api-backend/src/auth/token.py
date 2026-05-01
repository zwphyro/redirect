from jwt import PyJWTError, encode, decode

from datetime import timedelta
from src.auth.schemas import AccessTokenPayload, RefreshTokenPayload


class Token:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire: timedelta,
        refresh_token_expire: timedelta,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expire = access_token_expire
        self._refresh_token_expire = refresh_token_expire

    def create_access_token(self, data: AccessTokenPayload):
        access_token = encode(
            payload=data.model_dump_payload(self._access_token_expire),
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        return access_token

    def create_refresh_token(self, data: RefreshTokenPayload):
        refresh_token = encode(
            payload=data.model_dump_payload(self._refresh_token_expire),
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        return refresh_token

    def _decode_token_or_none(self, token: str):
        try:
            return decode(token, key=self._secret_key, algorithms=[self._algorithm])
        except PyJWTError:
            return None

    def decode_access_token(self, access_token: str):
        payload = self._decode_token_or_none(access_token)

        return None if payload is None else AccessTokenPayload(**payload)

    def decode_refresh_token(self, refresh_token: str):
        payload = self._decode_token_or_none(refresh_token)

        return None if payload is None else RefreshTokenPayload(**payload)
