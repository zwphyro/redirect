from fastapi import APIRouter, Query, status

from src.auth.dependencies import UserDependency
from src.redirect_link.dependencies import ServiceDependency
from src.redirect_link.schemas import CreateRedirectLinkSchema, RedirectLinkSchema
from src.schemas import HTTPExceptionSchema

router = APIRouter()


@router.get(
    "/",
    response_model=list[RedirectLinkSchema],
)
async def list_links(
    user: UserDependency,
    service: ServiceDependency,
    limit: int | None = Query(default=10, ge=1),
    offset: int | None = Query(default=None, ge=0),
):
    links = await service.list(user.id, limit=limit, offset=offset)
    return links


@router.get(
    "/{short_code}",
    response_model=RedirectLinkSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def get_link(short_code: str, user: UserDependency, service: ServiceDependency):
    link = await service.get_link(short_code, user.id)
    return link


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RedirectLinkSchema,
)
async def create_link(
    new_link: CreateRedirectLinkSchema, user: UserDependency, service: ServiceDependency
):
    link = await service.create_link(new_link.target_url, user.id)
    return link


@router.delete(
    "/{short_code}",
    response_model=RedirectLinkSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def delete_link(
    short_code: str, user: UserDependency, service: ServiceDependency
):
    link = await service.delete_link(short_code, user.id)
    return link


@router.put(
    "/active/{short_code}",
    response_model=RedirectLinkSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def toggle_active(
    short_code: str, user: UserDependency, service: ServiceDependency
):
    link = await service.toggle_active(short_code, user.id)
    return link
