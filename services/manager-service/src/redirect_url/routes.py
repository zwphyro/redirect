from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from src.redirect_url.schemas import CreateRedirectURLSchema, RedirectURLSchema

from src.redirect_url.service import RedirectURLService
from src.schemas import HTTPExceptionSchema

router = APIRouter()

ServiceDependency = Annotated[RedirectURLService, Depends(RedirectURLService)]


@router.get("/", response_model=list[RedirectURLSchema])
async def list_redirects(
    service: ServiceDependency,
    limit: int | None = Query(default=None, ge=1),
    offset: int | None = Query(default=None, ge=0),
):
    redirects = await service.list(limit=limit, offset=offset)

    return redirects


@router.get(
    "/{short_code}",
    response_model=RedirectURLSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def get_redirect(short_code: str, service: ServiceDependency):
    redirect = await service.get_redirect(short_code)

    # TODO: cache value

    return redirect


@router.post("/", response_model=RedirectURLSchema)
async def create_redirect(
    new_redirect: CreateRedirectURLSchema, service: ServiceDependency
):
    redirect = await service.create_redirect(new_redirect.original_url)

    # TODO: cache value

    return redirect


@router.delete(
    "/{short_code}",
    response_model=RedirectURLSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def delete_redirect(short_code: str, service: ServiceDependency):
    redirect = await service.delete_redirect(short_code)

    # TODO: invalidate cache

    return redirect


@router.put(
    "/active/{short_code}",
    response_model=RedirectURLSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def toggle_active(short_code: str, service: ServiceDependency):
    redirect = await service.toggle_active(short_code)

    # TODO: invalidate cache

    return redirect
