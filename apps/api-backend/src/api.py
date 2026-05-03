from fastapi import APIRouter, Depends, status
from src.auth.dependencies import authenticate
from src.auth.routes import router as auth_router
from src.redirect_link.routes import router as redirect_link_router
from src.schemas import HTTPExceptionSchema

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(
    redirect_link_router,
    prefix="/redirect_links",
    tags=["Redirect links"],
    dependencies=[Depends(authenticate)],
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema}},
)
