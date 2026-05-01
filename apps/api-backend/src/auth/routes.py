from fastapi import APIRouter, Depends, status
from pyrate_limiter import Limiter, Rate, Duration
from fastapi_limiter.depends import RateLimiter

from src.auth.dependencies import ServiceDependency, UserDependency
from src.auth.schemas import (
    CreateUserSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    TokenPairSchema,
    UserSchema,
)
from src.schemas import HTTPExceptionSchema

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(3, Duration.MINUTE))))],
)
async def register(new_user: CreateUserSchema, service: ServiceDependency):
    await service.register(new_user.email, new_user.password)


@router.post(
    "/login",
    response_model=TokenPairSchema,
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(3, Duration.MINUTE))))],
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema}},
)
async def login(user: LoginUserSchema, service: ServiceDependency):
    access_token, refresh_token = await service.login(user.email, user.password)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh",
    response_model=TokenPairSchema,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema}},
)
async def refresh(refresh_data: RefreshTokenSchema, service: ServiceDependency):
    access_token, refresh_token = await service.refresh(refresh_data.refresh_token)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.get(
    "/me",
    response_model=UserSchema,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema}},
)
async def get_me(user: UserDependency):
    return user
