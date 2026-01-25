from fastapi import APIRouter, HTTPException, status

from src.redirect_url.exceptions import RedirectURLNotFoundException
from src.redirect_url.schemas import CreateRedirectURLSchema, RedirectURLSchema
from src.dependencies import DBDependency

from src.redirect_url import service
from src.schemas import HTTPExceptionSchema

router = APIRouter()


@router.get("/", response_model=list[RedirectURLSchema])
async def list_redirects(session: DBDependency):
    # TODO: add pagination
    redirects = await service.list_redirects(session)
    return redirects


@router.get(
    "/{short_code}",
    response_model=RedirectURLSchema,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema}},
)
async def get_redirect(short_code: str, session: DBDependency):
    try:
        redirect = await service.get_redirect(short_code, session)
    except RedirectURLNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Redirect URL not found"
        )

    # TODO: cache value

    return redirect


@router.post("/", response_model=RedirectURLSchema)
async def create_redirect(new_redirect: CreateRedirectURLSchema, session: DBDependency):
    redirect = await service.create_redirect(new_redirect.original_url, session)

    # TODO: cache value

    return redirect


@router.delete("/{short_code}")
async def delete_redirect(short_code: str, session: DBDependency):
    try:
        redirect = await service.delete_redirect(short_code, session)
    except RedirectURLNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Redirect URL not found"
        )

    # TODO: update cache

    return redirect
