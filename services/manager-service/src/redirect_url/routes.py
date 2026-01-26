from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.redirect_url.schemas import CreateRedirectURLSchema, RedirectURLSchema

from src.redirect_url.service import RedirectURLService
from src.schemas import HTTPExceptionSchema

router = APIRouter()

ServiceDependency = Annotated[RedirectURLService, Depends(RedirectURLService)]


@router.get("/", response_model=list[RedirectURLSchema])
async def list_redirects(
    service: ServiceDependency,
    limit: int | None = None,
    offset: int | None = None,
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
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def delete_redirect(short_code: str, service: ServiceDependency):
    redirect = await service.delete_redirect(short_code)

    # TODO: invalidate cache

    return redirect


@router.put(
    "/{id}",
    response_model=RedirectURLSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def toggle_is_active(id: int, service: ServiceDependency):
    redirect = await service.toggle_is_active(id)

    # TODO: invalidate cache

    return redirect
