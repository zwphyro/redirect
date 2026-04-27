from fastapi import APIRouter, Query, status

from src.redirect_link.dependencies import ServiceDependency
from src.redirect_link.schemas import CreateRedirectLinkSchema, RedirectLinkSchema
from src.schemas import HTTPExceptionSchema

router = APIRouter()


@router.get("/", response_model=list[RedirectLinkSchema])
async def list_links(
    service: ServiceDependency,
    limit: int | None = Query(default=None, ge=1),
    offset: int | None = Query(default=None, ge=0),
):
    redirects = await service.list(limit=limit, offset=offset)
    return redirects


@router.get(
    "/{short_code}",
    response_model=RedirectLinkSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def get_link(short_code: str, service: ServiceDependency):
    redirect = await service.get_link(short_code)
    return redirect


@router.post("/", response_model=RedirectLinkSchema)
async def create_link(new_link: CreateRedirectLinkSchema, service: ServiceDependency):
    redirect = await service.create_link(new_link.target_url)
    return redirect


@router.delete(
    "/{short_code}",
    response_model=RedirectLinkSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def delete_link(short_code: str, service: ServiceDependency):
    redirect = await service.delete_link(short_code)
    return redirect


@router.put(
    "/active/{short_code}",
    response_model=RedirectLinkSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def toggle_active(short_code: str, service: ServiceDependency):
    redirect = await service.toggle_active(short_code)
    return redirect
