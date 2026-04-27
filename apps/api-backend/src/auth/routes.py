from fastapi import APIRouter, status

from src.auth.dependencies import ServiceDependency, UserDependency
from src.auth.schemas import (
    CreateUserSchema,
    RefreshTokenSchema,
    TokenPairSchema,
    UserSchema,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(new_user: CreateUserSchema, service: ServiceDependency):
    await service.register(new_user.email, new_user.password)


@router.post("/login", response_model=TokenPairSchema)
async def login(user: CreateUserSchema, service: ServiceDependency):
    access_token, refresh_token = await service.login(user.email, user.password)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh(refresh_data: RefreshTokenSchema, service: ServiceDependency):
    access_token, refresh_token = await service.refresh(refresh_data.refresh_token)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserSchema)
async def get_me(user: UserDependency):
    return user
