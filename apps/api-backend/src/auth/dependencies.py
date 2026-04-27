from datetime import timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pwdlib import PasswordHash

from src.auth.cryptography import get_hash
from src.auth.models import User
from src.auth.service import AuthService
from src.auth.token import Token
from src.dependencies import UOWDependency

HashDependency = Annotated[PasswordHash, Depends(get_hash)]


def get_token():
    return Token(
        secret_key="secret",
        algorithm="HS256",
        access_token_expire=timedelta(minutes=10),
        refresh_token_expire=timedelta(days=30),
    )


TokenDependency = Annotated[Token, Depends(get_token)]


def get_auth_service(
    uow: UOWDependency,
    hash: HashDependency,
    token: TokenDependency,
):
    return AuthService(uow, hash, token)


ServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    service: ServiceDependency,
):
    user = await service.get_current_user(auth.credentials)
    return user


UserDependency = Annotated[User, Depends(get_current_user)]
