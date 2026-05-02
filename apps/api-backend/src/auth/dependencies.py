from datetime import timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pwdlib import PasswordHash

from src.auth.cryptography import get_password_hash
from src.auth.models import User
from src.auth.service import AuthService
from src.auth.token import Token
from src.dependencies import UOWDependency
from src.settings import get_settings

PasswordHashDependency = Annotated[PasswordHash, Depends(get_password_hash)]


def get_token():
    settings = get_settings()
    return Token(
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        access_token_expire=timedelta(minutes=settings.access_token_expire_minutes),
        refresh_token_expire=timedelta(days=settings.refresh_token_expire_days),
    )


TokenDependency = Annotated[Token, Depends(get_token)]


def get_auth_service(
    uow: UOWDependency,
    password_hash: PasswordHashDependency,
    token: TokenDependency,
):
    return AuthService(uow, password_hash, token)


ServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


async def authenticate(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    service: ServiceDependency,
):
    user = await service.get_current_user(auth.credentials)
    return user


UserDependency = Annotated[User, Depends(authenticate)]
